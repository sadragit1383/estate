from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from ..models.user_model import User
from ..models.useage_model import UserStatusChoices,UserUseage
from apps.core.authentication.accesstoken.authentication import CustomJWTAuthentication
from django.utils import timezone


class UserStatusView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        status_value = request.data.get("status")

        if status_value not in UserStatusChoices.values:
            return Response({"error": "وضعیت نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        if status_value == UserStatusChoices.ENTERED:
            # ورود: فقط startTime ذخیره می‌شود
            usage = UserUseage.objects.create(user=user, status=status_value)
            return Response({"message": "ورود ثبت شد.", "id": usage.id}, status=status.HTTP_201_CREATED)

        elif status_value == UserStatusChoices.EXITED:
            # خروج: باید رکورد قبلی پیدا شود و زمان پایان تنظیم شود
            try:
                usage = UserUseage.objects.filter(user=user, status=UserStatusChoices.ENTERED).latest('startTime')
            except UserUseage.DoesNotExist:
                return Response({"error": "هیچ زمان شروعی برای کاربر ثبت نشده."}, status=status.HTTP_404_NOT_FOUND)

            usage.endTime = timezone.now()
            usage.status = UserStatusChoices.EXITED
            usage.save()
            return Response({"message": "خروج ثبت شد.", "result": usage.result}, status=status.HTTP_200_OK)

        else:
            # وضعیت‌های دیگر مثل active
            UserUseage.objects.create(user=user, status=status_value, startTime=timezone.now())
            return Response({"message": "وضعیت ثبت شد."}, status=status.HTTP_201_CREATED)