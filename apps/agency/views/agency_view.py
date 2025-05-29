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
from apps.user.models.permissions.user_permission import IsAgencyOwner
from ..models.agency_model import Agency

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
                "createdAt": req.created_at.strftime("%Y-%m-%d %H:%M"),
                "isActive": req.isActive,
            }
            for req in requests.order_by('-created_at')
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