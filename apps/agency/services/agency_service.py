from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from apps.user.models.user_model import User
from ..models.requestagency_model import RequestCollaborationAgency
from ..models.agency_model import Consultant,Manager

class CollaborationService:
    @staticmethod
    @transaction.atomic
    def create_collaboration_request(agency_user, mobileNumber, role, message=None):
        try:
            target_user = User.objects.get(mobileNumber=mobileNumber)
        except User.DoesNotExist:
            raise User.DoesNotExist("کاربر مورد نظر یافت نشد")

        # بررسی وضعیت شغلی فعلی کاربر
        is_consultant_active = Consultant.objects.filter(user=target_user, isActive=True).exists()
        is_manager_active = Manager.objects.filter(user=target_user, isActive=True).exists()

        if is_consultant_active or is_manager_active:
            raise ValidationError("کاربر قبلاً در یک آژانس دیگر مشغول به کار است")

        # ساخت و ذخیره درخواست همکاری
        request = RequestCollaborationAgency(
            agency=agency_user.agency,
            user=target_user,
            role=role,
            request_message=message
        )

        request.full_clean()  # اعتبارسنجی مدل
        request.save()        # ذخیره در پایگاه داده

        return request

