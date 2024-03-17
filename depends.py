from repositories.rooms import RoomRepository
from repositories.users import UserRepository
from services.rooms import RoomService
from services.users import UserService


def get_user_service() -> UserService:
    user_repository = UserRepository()
    user_service = UserService(user_repository)
    return user_service


def get_room_service() -> RoomService:
    room_repository = RoomRepository()
    room_service = RoomService(room_repository)
    return room_service
