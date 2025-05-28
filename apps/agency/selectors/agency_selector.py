from ..models.requestagency_model import RequestCollaborationAgency

class CollaborationSelector:
    
    @staticmethod
    def get_user_requests(user):
        return RequestCollaborationAgency.objects.filter(user=user)

    @staticmethod
    def get_agency_requests(agency):
        return RequestCollaborationAgency.objects.filter(agency=agency)