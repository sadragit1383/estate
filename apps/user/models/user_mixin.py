class UserMethodsMixin:
    def get_full_name(self):
        full_name = f"{self.firstName or ''} {self.lastName or ''}".strip()
        if not full_name:
            return "کاربر"
        return full_name

    def is_admin(self):
        return self.role.slug == 'admin' or self.is_superuser

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def activate_user_info(self):
        if hasattr(self, 'usersecret'):
            self.usersecret.isInfoFiled = True
            self.usersecret.isActive = True
            self.usersecret.save()

    def deactivate(self):
        if hasattr(self, 'usersecret'):
            self.usersecret.isActive = False
            self.usersecret.save()