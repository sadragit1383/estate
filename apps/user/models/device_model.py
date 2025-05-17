from django.db import models
from user_model import User

class DeviceInfo(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    userAgent = models.CharField(max_length=255)
    platform = models.CharField(max_length=50)
    screenWidth = models.IntegerField()
    screenHeight = models.IntegerField()
    deviceType = models.CharField(max_length=50)

    class Meta:

        db_table = 'DeviceInfo'
        app_lable = 'user_device'
