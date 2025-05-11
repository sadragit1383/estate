from django.db import models
import uuid
from .user_model import User


class Currency(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    isActive = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'currency'
        app_lable = 'userapp'



class Wallet(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.BigIntegerField(default=0)
    userId = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    isActive = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.BigIntegerField()
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE,verbose_name='نوع ارز')

    class Meta:
        db_table = 'user_wallet'
        app_lable = 'userapp'




