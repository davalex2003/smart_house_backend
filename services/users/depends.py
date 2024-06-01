from services.users.repositories.users import UserRepository
from services.users.services.users import UserService


def get_user_service() -> UserService:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service
