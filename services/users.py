from repositories.users import UserRepository
from schemas.users import User, UserValidate, UserUpdate


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User):
        self.repository.create_user(user)

    def validate_user(self, user: UserValidate) -> bool:
        return self.repository.validate_user(user)

    def validate_email(self, e_mail: str) -> bool:
        return self.repository.validate_email(e_mail)

    def delete_user(self, e_mail: str):
        self.repository.delete_user(e_mail)

    def update_user(self, user: UserUpdate):
        self.repository.update_user(user)
