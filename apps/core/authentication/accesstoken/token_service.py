# core/services/token_service.py
from abc import ABC, abstractmethod


class AbstractTokenService(ABC):
    @abstractmethod
    def generate_access_token(self, user):
        pass

    @abstractmethod
    def refresh_token(self, refresh_token):
        pass