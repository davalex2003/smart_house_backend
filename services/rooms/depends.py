from services.rooms.repositories.rooms import RoomRepository
from services.rooms.services.rooms import RoomService


def get_room_service() -> RoomService:
    room_repository = RoomRepository()
    room_service = RoomService(room_repository)
    return room_service
