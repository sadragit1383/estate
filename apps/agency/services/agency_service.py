from django.db import transaction, IntegrityError
from django.core.exceptions import ValidationError
from apps.user.models.user_model import User
from ..models.requestagency_model import RequestCollaborationAgency

class CollaborationService:
    @staticmethod
    @transaction.atomic
    def create_collaboration_request(agency_user, mobileNumber, role, message=None):
    
            target_user = User.objects.get(mobileNumber=mobileNumber)

            # شیء رو می‌سازیم ولی ذخیره نمی‌کنیم
            request = RequestCollaborationAgency(
                agency=agency_user.agency,
                user=target_user,
                role=role,
                request_message=message
            )

            request.full_clean()  # اجرای اعتبارسنجی‌ها
            request.save()        # ذخیره در دیتابیس
            return request



