from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models.user_model import User
from serializers.user_serializer import SignupSerializer
from models.user_model import UserManager
import response_handler
import utils


class RegisterOrLoginUserAPIView(APIView):

    def post(self, request):
        mobile_number = request.data.get("mobile_number")

        if not mobile_number:
            return response_handler.ResponseHandler.error(
                message="شماره موبایل الزامی است.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
            
        user_manager = UserManager()
        try:
            user_exists = user_manager.check_user(mobile_number)

            if user_exists:
                user = user_manager.get_user(mobile_number)
            else:
                user = user_manager.create_user(mobile_number=mobile_number)

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
            return response_handler.ResponseHandler.error(
                message=str(exc),
                status_code=status.HTTP_400_BAD_REQUEST
            )