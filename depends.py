from repositories.devices import DeviceRepository
from repositories.rooms import RoomRepository
from repositories.users import UserRepository
from services.devices import DeviceService
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


def get_device_service() -> DeviceService:
    device_repository = DeviceRepository()
    device_service = DeviceService(device_repository)
    return device_service
