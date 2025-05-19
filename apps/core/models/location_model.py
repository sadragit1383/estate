
from django.db import models
import uuid

class Country(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # تغییر ID به UUID
    name = models.CharField(max_length=100, verbose_name='نام کشور', blank=True, null=True)
    slug = models.CharField(max_length=100, verbose_name='نامک', blank=True, null=True)


    def __str__(self):
        return self.name



class Province(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='نام استان', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name='کشور', related_name='provinces', blank=True, null=True)
    slug = models.CharField(max_length=100, verbose_name='نامک', blank=True, null=True)



    def __str__(self):
        return self.name



class City(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='نام شهر', blank=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name='استان', related_name='cities', blank=True, null=True)
    slug = models.CharField(max_length=100, verbose_name='نامک', blank=True, null=True)



    def __str__(self):
        return self.name




class Area(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='نام محله', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='شهر', related_name='neighborhoods', blank=True, null=True)
    slug = models.CharField(max_length=100, verbose_name='نامک', blank=True, null=True)


    def __str__(self):
        return self.name

