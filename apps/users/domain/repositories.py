from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    @abstractmethod
    def create(self, data: dict):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def get_by_id(self, user_id: int):
        pass

    @abstractmethod
    def update(self, user, data: dict):
        pass

    @abstractmethod
    def delete(self, user):
        pass

    @abstractmethod
    def get_by_email(self, email: str):
        pass