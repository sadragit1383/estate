from celery import shared_task
from PIL import Image
import os
from django.conf import settings
from ..models import AdvertisementGallery

@shared_task(bind=True, max_retries=3)
def process_advertisement_gallery_images(self, gallery_id):


    try:
        
        ag = AdvertisementGallery.objects.get(id=gallery_id)

        if not ag.org_image:
            return "No original image"

        original_path = ag.org_image.path
        if not os.path.exists(original_path):
            return "Original image not found"

        sizes = [
            ('thumbnail_image', 'xs', 192, 108),
            ('small_image', 'sm', 320, 170),
            ('medium_image', 'md', 768, 480),
            ('large_image', 'lg', 1280, 768),
        ]

        for field, folder, w, h in sizes:
            if getattr(ag, field):
                continue

            output_path = os.path.join(
                settings.MEDIA_ROOT,
                f'advertisement_gallery/{folder}/{ag.id}.jpg'
            )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            try:

                img = Image.open(original_path)
                img = img.convert('RGB') if img.mode in ('RGBA', 'P') else img
                img.thumbnail((w, h), Image.LANCZOS)
                img.save(output_path, 'JPEG', quality=90)

                rel_path = os.path.relpath(output_path, settings.MEDIA_ROOT)
                setattr(ag, field, rel_path)

            except Exception as err:
                print(f"Error processing {field}: {err}")
                continue

        ag.save()
        return f"Images processed for {gallery_id}"

    except Exception as e:
        print(f"Retrying task for {gallery_id}, error: {e}")
        self.retry(exc=e, countdown=60)
