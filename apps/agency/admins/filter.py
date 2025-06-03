import django_filters
from ..models.requestagency_model import RequestCollaborationAgency

class RequestCollaborationAgencyFilter(django_filters.FilterSet):
    class Meta:
        model = RequestCollaborationAgency
        fields = {
            'status': ['exact'],
            'role': ['exact'],
            'isActive': ['exact'],
            'agency': ['exact'],
            'user': ['exact'],
            'createdAt': ['date__gte', 'date__lte'],
        }



