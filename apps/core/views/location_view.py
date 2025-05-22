from rest_framework import generics
from ..models.location_model import Country, Province, City, Area
from ..serializers.location_serializers import CountrySerializer, ProvinceSerializer, CitySerializer, AreaSerializer,UserLocationSerializer
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response
from ..authentication.accesstoken.authentication import CustomJWTAuthentication

class CountryListView(generics.ListAPIView):

    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class ProvinceListView(generics.ListAPIView):
    serializer_class = ProvinceSerializer

    def get_queryset(self):
        country_id = self.kwargs['countryId']
        return Province.objects.filter(country_id=country_id)


class CityListView(generics.ListAPIView):
    serializer_class = CitySerializer

    def get_queryset(self):
        province_id = self.kwargs['provinceId']
        return City.objects.filter(province_id=province_id)


class AreaListView(generics.ListAPIView):
    serializer_class = AreaSerializer

    def get_queryset(self):
        city_id = self.kwargs['cityId']
        return Area.objects.filter(city_id=city_id)



class UserLocationCreateView(APIView):

    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def post(self, request):
        serializer = UserLocationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "موقعیت مکانی با موفقیت ثبت شد."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)