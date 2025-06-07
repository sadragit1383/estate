from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models.advertisement import Advertisement, SecretAdvertisement

@receiver(post_save, sender=Advertisement)
def create_secret_advertisement(sender, instance, created, **kwargs):
    if created:
        SecretAdvertisement.objects.create(advertisement=instance)