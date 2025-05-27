from typing import Dict, Any
from django.core.exceptions import ValidationError
from ...models.agency_model import Agency
from apps.core.models.location_model import Province,City
from apps.user.models.user_model import User
from django.core.files import File
from typing import Optional
from apps.core.models.service_location import parse_location_slugs

class AgencyService:

    @staticmethod
    def create_agency(
        user: User,
        name: str,
        address: str,
        profile_image: Optional[File] = None,
        licence_image: Optional[File] = None,
        email: Optional[str] = None,
        bio: Optional[str] = None,
        time_work: Optional[str] = None,
        location_slugs: Optional[str] = None,
        banner_image: Optional[File] = None,
        logo_image: Optional[File] = None,
    ) -> Agency:


        if not user or not name or not address:
            raise ValidationError("User, name and address are required fields")

        province = None
        cities = []

        if location_slugs:
            slugs = parse_location_slugs(location_slugs)
            if slugs:
                try:
                    province = Province.objects.get(slug=slugs[0])
                    cities = City.objects.filter(slug__in=slugs[1:], province=province)
                except Province.DoesNotExist:
                    raise ValidationError("Invalid province slug")
                except City.DoesNotExist:
                    raise ValidationError("One or more city slugs are invalid")

        agency = Agency(
            user=user,
            name=name,
            address=address,
            email=email,
            bio=bio,
            timeWork=time_work,
            province=province,
            status=Agency.Status.INACTIVE
        )


        agency.full_clean()
        agency.save()

        # ذخیره تصاویر
        if profile_image:
            agency.profileImage = profile_image
        if licence_image:
            agency.licenceImage = licence_image
        if banner_image:
            agency.bannerImage = banner_image
        if logo_image:
            agency.logoImage = logo_image

        agency.save()

        # اضافه کردن شهرها (ManyToMany)
        if cities:
            agency.cities.set(cities)

        return agency

    @staticmethod
    def update_agency(
        agency: Agency,
        name: Optional[str] = None,
        address: Optional[str] = None,
        profile_image: Optional[File] = None,
        licence_image: Optional[File] = None,
        email: Optional[str] = None,
        bio: Optional[str] = None,
        time_work: Optional[str] = None,
        location_slugs: Optional[str] = None,
        banner_image: Optional[File] = None,
        logo_image: Optional[File] = None,
    ) -> Agency:


        if name is not None:
            agency.name = name
        if address is not None:
            agency.address = address
        if email is not None:
            agency.email = email
        if bio is not None:
            agency.bio = bio
        if time_work is not None:
            agency.timeWork = time_work

        # پردازش location_slugs
        if location_slugs is not None:
            slugs = parse_location_slugs(location_slugs)
            if slugs:
                try:
                    province = Province.objects.get(slug=slugs[0])
                    cities = City.objects.filter(slug__in=slugs[1:], province=province)
                    agency.province = province
                    agency.cities.set(cities)
                except Province.DoesNotExist:
                    raise ValidationError("Invalid province slug")
                except City.DoesNotExist:
                    raise ValidationError("One or more city slugs are invalid")
            else:
                agency.province = None
                agency.cities.clear()

        # به‌روزرسانی تصاویر
        if profile_image is not None:
            agency.profileImage = profile_image
        if licence_image is not None:
            agency.licenceImage = licence_image
        if banner_image is not None:
            agency.bannerImage = banner_image
        if logo_image is not None:
            agency.logoImage = logo_image

        agency.save()
        return agency