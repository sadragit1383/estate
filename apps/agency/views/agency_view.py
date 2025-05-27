from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from  ..models.service.agency_service import AgencyService
from apps.core.authentication.accesstoken.authentication import CustomJWTAuthentication


class AgencyCreateAPIView(APIView):

    authentication_classes = [CustomJWTAuthentication]

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]


    def post(self, request):
        try:
            agency = AgencyService.create_agency(
                user=request.user,
                name=request.data.get('name'),
                address=request.data.get('address'),
                email=request.data.get('email'),
                bio=request.data.get('bio'),
                time_work=request.data.get('timeWork'),
                location_slugs=request.data.get('location'),  # همان رشته JSON را مستقیم می‌فرستیم
                profile_image=request.FILES.get('profileImage'),
                licence_image=request.FILES.get('licenceImage'),
                banner_image=request.FILES.get('bannerImage'),
                logo_image=request.FILES.get('logoImage')
            )
            return Response({
                'status': 'success',
                'data': {
                    'agency_id': agency.user_id,
                    'name': agency.name
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)