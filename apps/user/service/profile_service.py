# user/services/profile_service.py
from ..models.user_model import UserValidator
from ..models.user_model import RoleUser, User


class ProfileUpdater:
    def __init__(self, user, data):
        self.user = user
        self.data = data

    def update_profile(self):
        try:
            for field, value in self.data.items():
                setattr(self.user, field, value)
            self.user.full_clean()  # Run model field validators
            self.user.save()
            return True, "پروفایل با موفقیت به‌روزرسانی شد."
        except Exception as e:
            return False, str(e)






class AdminRegistrationService:
    def __init__(self, user_model=None):
        self.user_model = user_model or User

    def execute(self, mobile, password, first_name, last_name):
        if self.user_model.objects.check_user(mobile):
            raise ValueError("کاربر از قبل وجود دارد.")

        UserValidator.validate_mobileNumber(mobile)
        UserValidator.validate_password(password)

        role, _ = RoleUser.objects.get_or_create(
            slug='admin',
            defaults={"title": "Administrator", "isActive": True}
        )

        user = self.user_model.objects.create_user(
            mobileNumber=mobile,
            password=password,
            firstName=first_name,
            lastName=last_name,
            email=f"{mobile}@admin.com",
            is_superuser=True,
            is_staff=True,
            role=role
        )
        return user



class AdminPasswordChangeService:
    def __init__(self, user):
        self.user = user

    def change_password(self, old_password, new_password):
        if not self.user.check_password(old_password):
            raise ValueError("رمز عبور فعلی نادرست است.")

        UserValidator.validate_password(new_password)

        self.user.set_password(new_password)
        self.user.save()