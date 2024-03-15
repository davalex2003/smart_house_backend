from typing import List

from repositories.users import UserRepository
from schemas.users import User


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user: User):
        self.repository.create_user(user)
