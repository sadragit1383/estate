from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from  ..models.service.agency_service import AgencyService
from apps.core.authentication.accesstoken.authentication import CustomJWTAuthentication
from ..models.requestagency_model import StatusResponse,RequestCollaborationAgency
from apps.user.response_handler import ResponseHandler
from apps.user.models.permissions.user_permission import IsAgencyOwner,IsAdmin
from ..models.agency_model import Agency,RejectedAgency,SubjectBan
from django.utils.decorators import method_decorator
from apps.user.models.user_model import banUsers
import utils
from ..serializers.agency_serializers import RejectAgencySerializer,AgencyDetailSerializer
from uuid import UUID
import logging
logger = logging.getLogger(__name__)
from ..serializers.agency_serializers import UpdateAgencySerializer

class AgencyCreateAPIView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):
        try:
            agency = AgencyService.create_agency(
                user=request.user,
                name=request.data.get('name'),
                address=request.data.get('address'),
                email=request.data.get('email'),
                bio=request.data.get('bio'),
                time_work=request.data.get('timeWork'),
                location_slugs=request.data.get('location'),  # همان رشته JSON را مستقیم می‌فرستیم
                profile_image=request.FILES.get('profileImage'),
                licence_image=request.FILES.get('licenceImage'),
                banner_image=request.FILES.get('bannerImage'),
                logo_image=request.FILES.get('logoImage')
            )

            return Response({
                'status': 'success',
                'data': {
                    'agencyId': agency.user_id,
                    'name': agency.name
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(utils.rate_limit_ip(max_requests=1000, time_frame_hours=24), name='dispatch')

class CollaborationRequestAgencyAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAgencyOwner]

    def get(self, request):
        agency = request.user.agency
        status_param = request.query_params.get('status')

        requests = RequestCollaborationAgency.objects.filter(agency=agency).select_related('user')

        if status_param:
            status_param = status_param.lower()
            valid_statuses = [choice[0] for choice in StatusResponse.choices]
            if status_param not in valid_statuses:
                return ResponseHandler.error(
                    message="وضعیت ارسال‌شده معتبر نیست",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    code="invalid_status"
                )
            requests = requests.filter(status=status_param)

        # ساخت خروجی
        data = [
            {
                "id": str(req.id),
                "FullName": req.user.get_full_name(),
                "mobileNumber": req.user.mobileNumber,
                "role": req.get_role_display(),
                "status": req.get_status_display(),
                "createdAt": req.createdAt.strftime("%Y-%m-%d %H:%M"),
                "isActive": req.isActive,
            }
            for req in requests.order_by('-createdAt')
        ]

        return ResponseHandler.success(
            data=data,
            message='اطلاعات با موفقیت واکشی شد'

                                       )


class DeactivateAgencyMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get('userId')

        if not user_id:
            return Response({'error': 'شناسه کاربر ارسال نشده است'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            agency = Agency.objects.get(user=request.user)
        except Agency.DoesNotExist:
            return Response({'error': 'آژانس یافت نشد'}, status=status.HTTP_404_NOT_FOUND)

        if request.user != agency.user:
            return Response({'error': 'شما اجازه انجام این عملیات را ندارید'}, status=status.HTTP_403_FORBIDDEN)

        try:
            agency.deactivate_member(user_id)
            return Response({'success': 'کاربر با موفقیت غیرفعال شد'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class RejectAgencyAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def post(self, request):
        serializer = RejectAgencySerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            agency_id = serializer.validated_data['agency']['id']
            text = serializer.validated_data['text']

            # پیدا کردن آژانس
            agency = Agency.objects.get(pk=agency_id)

            # رد کردن آژانس
            agency.status = Agency.Status.REJECTED
            agency.save()

            # ذخیره در RejectedAgency
            RejectedAgency.objects.create(
                agency=agency,
                text=text
            )

            # ذخیره در banUsers
            banUsers.objects.create(
                user=agency.user,
                text=text,
                banSubject=SubjectBan.AGENCY
            )

            return Response(
                {'detail': 'آژانس با موفقیت رد شد.'},
                status=status.HTTP_200_OK
            )

        except Agency.DoesNotExist:
            return Response(
                {'detail': 'آژانس مورد نظر یافت نشد.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class AgencyConfirmationAPIView(APIView):
    """
    API View برای تایید آژانس توسط ادمین
    """
    permission_classes = [IsAdmin]  # فقط کاربران ادمین می‌توانند آژانس‌ها را تایید کنند

    def post(self, request):
        try:
            agency_id = request.data.get('agencyId')

            # اعتبارسنجی وجود agencyId در بدنه درخواست
            if not agency_id:
                return Response(
                    {'success': False, 'message': 'فیلد agencyId الزامی است'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # اعتبارسنجی فرمت UUID
            try:
                agency_uuid = UUID(agency_id)
            except ValueError:
                return Response(
                    {'success': False, 'message': 'فرمت agencyId نامعتبر است'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # فراخوانی متد confirm_agency از مدل Agency
            success, message = Agency.confirm_agency(agency_uuid)

            if success:
                return Response(
                    {'success': True, 'message': message},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'success': False, 'message': message},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            logger.error(f"خطا در تایید آژانس: {str(e)}", exc_info=True)
            return Response(
                {'success': False, 'message': 'خطای سرور در پردازش درخواست'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class AgencyAPIView(APIView):
    """
    API برای دریافت اطلاعات آژانس (فقط برای آژانس لاگین شده)
    """
    permission_classes = [IsAuthenticated,IsAgencyOwner]

    def get(self, request):
        try:
            # دریافت آژانس مربوط به کاربر لاگین شده
            agency = Agency.objects.select_related(
                'user', 'province'
            ).prefetch_related(
                'cities',
                'consultants__user',
                'managers__user'
            ).get(user=request.user)

            serializer = AgencyDetailSerializer(agency)
            return Response({
                'success': True,
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Agency.DoesNotExist:
            return Response({
                'success': False,
                'message': 'شما به عنوان آژانس ثبت نشده‌اید'
            }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UpdateAgencyAPIView(APIView):
    
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # برای آپلود عکس‌ها

    def put(self, request):
        try:
            agency = Agency.objects.get(user=request.user)
        except Agency.DoesNotExist:
            return Response({"detail": "آژانس یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateAgencySerializer(agency, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "اطلاعات با موفقیت به‌روزرسانی شد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
