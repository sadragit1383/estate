# user/services/profile_service.py

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
