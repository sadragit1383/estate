from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models.advertisement import Advertisement, SecretAdvertisement
from ..models.gallery import AdvertisementGallery
from ..tasks.task import process_advertisement_gallery_images

@receiver(post_save, sender=Advertisement)
def create_secret_advertisement(sender, instance, created, **kwargs):
    if created:
        SecretAdvertisement.objects.create(advertisement=instance)




@receiver(post_save, sender=AdvertisementGallery)
def trigger_image_processing(sender, instance, created, **kwargs):
    if created and instance.org_image:
        process_advertisement_gallery_images.delay(str(instance.id))
