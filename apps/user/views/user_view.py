from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.user_model import User
from ..serializers.user_serializer import SignupSerializer
from ..models.user_model import UserManager
from ..response_handler import ResponseHandler
from django.core.exceptions import ValidationError
import utils
from ..models.validation.user_validation import ValidMobileNumber
import utils
from django.utils.decorators import method_decorator
from ..models.accessToken.token_service_factory import TokenServiceFactory


@method_decorator(utils.rate_limit_ip(max_requests=1000, time_frame_hours=1), name='dispatch')

class RegisterOrLoginUserAPIView(APIView):

    def post(self, request):
        mobileNumber = request.data.get("mobileNumber")

        if not mobileNumber:
            return ResponseHandler.error(
                message="شماره موبایل الزامی است.",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        user_manager = User.objects
        try:
            user_exists = user_manager.check_user(mobileNumber)

            if user_exists:
                user = user_manager.get_user(mobileNumber)
            else:
                user = user_manager.create_user(mobileNumber=mobileNumber)

            user_secret = user_manager.create_user_secret(user)

            return Response(
                {
                    "fullName": user.get_full_name() or "",
                    "activeCode": user_secret.activeCode,
                    "mobileNumber": user.mobileNumber,
                    "message": "کد تایید برای موبایل همراه شما ارسال شد."
                },
                status=status.HTTP_201_CREATED if not user_exists else status.HTTP_200_OK
            )

        except ValueError as exc:
            return ResponseHandler.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(utils.rate_limit_ip(max_requests=1000, time_frame_hours=1), name='dispatch')

class OTPVerifyAPIView(APIView):

    def post(self, request):
        mobile_number = request.data.get('mobileNumber')
        active_code = request.data.get('activeCode')

        # Validate input
        if not mobile_number or not active_code:
            return ResponseHandler.error(
                message="Both mobileNumber and activeCode are required.",
                code="missing_parameters",
                status_code=400
            )

        try:
            ValidMobileNumber(mobile_number)
        except ValidationError as e:
            return ResponseHandler.error(
                message=str(e),
                code="invalid_mobile",
                status_code=400
            )

        # Delegate verification to model layer
        user, message, status_code = User.objects.verify_user_otp(mobile_number, active_code)

        if not user:
            error_code = {
                403: "invalid_otp",
                404: "user_not_found",
                410: "otp_expired"
            }.get(status_code, "verification_failed")

            return ResponseHandler.error(
                message=message,
                code=error_code,
                status_code=status_code
            )

        # Generate access token
        token_service = TokenServiceFactory.get_service()
        access_token = token_service.generate_access_token(user)

        # Successful verification
        response_data = {
    'mobileNumber': user.mobileNumber,
    'firstName': user.get_full_name() or None,
    'access_token': str(access_token)
        }
        
        return ResponseHandler.success(
            data=response_data,
            message=message,
            status_code=status_code
        )

