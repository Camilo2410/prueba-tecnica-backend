from apps.users.infrastructure.repositories import DjangoUserRepository


class UserUseCases:
    def __init__(self, repository=None):
        self.repository = repository or DjangoUserRepository()

    def create_user(self, data: dict):
        return self.repository.create(data)

    def list_users(self):
        return self.repository.list()

    def retrieve_user(self, user_id: int):
        return self.repository.get_by_id(user_id)

    def update_user(self, user_id: int, data: dict):
        user = self.repository.get_by_id(user_id)
        return self.repository.update(user, data)

    def deactivate_user(self, user_id: int):
        user = self.repository.get_by_id(user_id)
        return self.repository.delete(user)