from ..models.user_model import User
from rest_framework import status,permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.core.authentication.accesstoken.token_service_factory import TokenServiceFactory
from apps.core.authentication.accesstoken.authentication import CustomJWTAuthentication
from ..models.permissions.user_permission import IsSuperUser,IsAdmin
from ..service.profile_service import *
from ..response_handler import ResponseHandler


class AdminLoginAPIView(APIView):
    def post(self, request):
        mobile_number = request.data.get("mobileNumber")
        password = request.data.get("password")

        # استفاده از متد سفارشی loginAdmin
        user_manager = User.objects  # فرض بر این است که loginAdmin روی model manager تعریف شده است
        result = user_manager.loginAdmin(mobile_number, password)

        if result is not True:
            return result

        user = user_manager.get_user(mobileNumber=mobile_number)

        token_service = TokenServiceFactory.get_service()
        access_token = token_service.generate_access_token(user)

        return Response({
            "message": "ادمین با موفقیت وارد پنل شد.",
            "accessToken": access_token,
            "fullName": user.get_full_name(),
        }, status=status.HTTP_200_OK)




class SigninAdminAPIView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated,IsSuperUser]

    def post(self, request):
        data = request.data
        try:
            user = AdminRegistrationService().execute(
                mobile=data.get("mobileNumber"),
                password=data.get("password"),
                first_name=data.get("firstName"),
                last_name=data.get("lastName"),
            )
            return ResponseHandler.success(
                message="ادمین با موفقیت ثبت شد.",
                data={"userId": str(user.id)},
            )
        except ValueError as e:
            return ResponseHandler.error(str(e), code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return ResponseHandler.error(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)



class ChangePasswordAdmin(APIView):

    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request):
        old_password = request.data.get("oldPassword")
        new_password = request.data.get("newPassword")

        if not old_password or not new_password:
            return ResponseHandler.error("رمزهای عبور الزامی هستند.", code=status.HTTP_400_BAD_REQUEST)

        try:
            AdminPasswordChangeService(request.user).change_password(old_password, new_password)
            return ResponseHandler.success("رمز عبور با موفقیت تغییر کرد.")
        except ValueError as e:
            return ResponseHandler.error(str(e), code=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return ResponseHandler.error(str(e), code=status.HTTP_500_INTERNAL_SERVER_ERROR)
