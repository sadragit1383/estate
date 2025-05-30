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
    test_field = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'currency'




class Wallet(models.Model):

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    balance = models.BigIntegerField(default=0)
    user = models.OneToOneField(User,on_delete=models.CASCADE,verbose_name='کاربر')
    isActive = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    currency = models.ForeignKey(Currency,on_delete=models.CASCADE,verbose_name='نوع ارز',blank=True,null=True)

    class Meta:
        db_table = 'user_wallet'
        app_label = 'user'




