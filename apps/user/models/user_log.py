from django.db import models
from user_model import User
from django.utils import timezone
from datetime import timedelta

class UserLog(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر')
    code = models.CharField(max_length=5,verbose_name='کد خطا')
    endpoint = models.CharField(max_length=255, verbose_name='آدرس اندپوینت')
    message = models.TextField(verbose_name='تکست خطا',blank=True,null=True)
    count = models.PositiveIntegerField(verbose_name='تعداد دفعات',default=0)



class BlackList(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کابر')
    isBan = models.BooleanField(default=False,verbose_name='بلاک شده')
    createAt = models.DateTimeField(default=timezone.now,verbose_name='ساخته شده')
    ipAddress = models.CharField(max_length=1000,verbose_name='ادرس ایپی')
    expireSince = models.DateTimeField(default=lambda: timezone.now() + timedelta(days=3))


    def __str__(self):
        return f'{self.user.firstName}__{self.user.lastName}'


    class Meta:

        db_table = 'black_list'