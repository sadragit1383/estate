from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..serializers.request_serializers import CollaborationRequestSerializer,CollaborationResponseSerializer
from apps.user.models.permissions.user_permission import IsAgencyOwner
from ..services.agency_service import CollaborationService
from ..selectors.agency_selector import CollaborationSelector
from apps.user.models.user_model import User
from apps.user.response_handler import ResponseHandler  # فرض مسیر
from ..models.requestagency_model import RequestCollaborationAgency,StatusResponse

from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError



class CollaborationRequestAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAgencyOwner]

    def post(self, request):

        serializer = CollaborationRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            collaboration_request = CollaborationService.create_collaboration_request(
                agency_user=request.user,
                mobileNumber=serializer.validated_data['mobileNumber'],
                role=serializer.validated_data['role'],
                message=serializer.validated_data.get('request_message')
            )
            return ResponseHandler.success(
                message="درخواست همکاری با موفقیت ارسال شد",
                status_code=status.HTTP_201_CREATED
            )
        except User.DoesNotExist:
            return ResponseHandler.error(
                message="کاربر مورد نظر یافت نشد",
                status_code=status.HTTP_404_NOT_FOUND,
                code="user_not_found"
            )
        except Exception as e:
            return ResponseHandler.error(
                message=str(e),
                status_code=status.HTTP_400_BAD_REQUEST,
                code="bad_request"
            )

    def get(self, request):
        requests = CollaborationSelector.get_agency_requests(request.user.agency)
        data = [{
            "id": str(req.id),
            "user": req.user.get_full_name(),
            "role": req.role,
            "status": req.status
        } for req in requests]
        return ResponseHandler.success(data=data)


class CollaborationRequestListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        requests = CollaborationSelector.get_user_requests(request.user)

        data = [{
            "id": str(req.id),
            "agency": str(req.agency),  # اگر میخوای نام یا شناسه آژانس رو بذاری
            "role": req.role,
            "status": req.status,
            "requestMessage": req.request_message,
            "createdAt": req.created_at.isoformat() if req.created_at else None
        } for req in requests]

        return ResponseHandler.success(data=data,message='اطلاعات با موفقیت دریافت شد')




class CollaborationResponseAPIView(APIView):
    """
    API برای پاسخ دادن به درخواست همکاری اژانس
    فقط کاربری که درخواست برای او ارسال شده میتواند پاسخ دهد
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request_id = request.data.get('id')
            response_type = request.data.get('response_type')
            response_message = request.data.get('response_message', '')

            # بررسی وجود فیلدهای اجباری
            if not request_id:
                return Response({
                    'success': False,
                    'message': 'شناسه درخواست الزامی است',
                    'errors': {'id': ['این فیلد الزامی است']}
                }, status=status.HTTP_400_BAD_REQUEST)

            if not response_type:
                return Response({
                    'success': False,
                    'message': 'نوع پاسخ الزامی است',
                    'errors': {'response_type': ['این فیلد الزامی است']}
                }, status=status.HTTP_400_BAD_REQUEST)

            # بررسی معتبر بودن نوع پاسخ
            valid_responses = ['accepted', 'rejected']
            if response_type not in valid_responses:
                return Response({
                    'success': False,
                    'message': 'نوع پاسخ نامعتبر است',
                    'errors': {'response_type': [f'باید یکی از این مقادیر باشد: {", ".join(valid_responses)}']}
                }, status=status.HTTP_400_BAD_REQUEST)

            # یافتن درخواست همکاری
            collaboration_request = get_object_or_404(
                RequestCollaborationAgency,
                id=request_id
            )

            # بررسی اینکه فقط کاربر مورد نظر بتواند پاسخ دهد
            if collaboration_request.user != request.user:
                return Response({
                    'success': False,
                    'message': 'شما مجاز به پاسخ دادن این درخواست نیستید'
                }, status=status.HTTP_403_FORBIDDEN)

            # بررسی وضعیت درخواست - فقط درخواست‌های در انتظار قابل پاسخ هستند
            if collaboration_request.status != StatusResponse.PENDING:
                return Response({
                    'success': False,
                    'message': 'این درخواست قبلاً پاسخ داده شده است'
                }, status=status.HTTP_400_BAD_REQUEST)

            # پردازش پاسخ
            if response_type == 'accepted':
                collaboration_request.accept(response_message)
                message = 'درخواست همکاری با موفقیت پذیرفته شد'
            elif response_type == 'rejected':
                collaboration_request.reject(response_message)
                message = 'درخواست همکاری رد شد'

            return Response({
                'success': True,
                'message': message,
                'data': {
                    'id': str(collaboration_request.id),
                    'status': collaboration_request.status,
                    'response_message': collaboration_request.response_message,
                    'updated_at': collaboration_request.updated_at
                }
            }, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({
                'success': False,
                'message': 'خطا در اعتبارسنجی داده‌ها',
                'errors': e.message_dict if hasattr(e, 'message_dict') else {'detail': [str(e)]}
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'success': False,
                'message': 'خطای داخلی سرور',
                'errors': {'detail': [str(e)]}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)