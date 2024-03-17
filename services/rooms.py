from typing import List

from repositories.rooms import RoomRepository
from schemas.rooms import RoomDTO, Room, RoomItem, RoomID
from schemas.users import UserValidate


class RoomService:

    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def create_room(self, room: Room) -> bool:
        user = UserValidate(e_mail=room.e_mail, hash_password=room.hash_password)
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return False
        user_id = user_id[0]
        room_dto = RoomDTO(name=room.name, user_id=user_id)
        self.repository.create_room(room_dto)
        return True

    def get_rooms(self, user: UserValidate) -> List[RoomItem]:
        user_id = self.repository.get_user_id(user)
        if user_id is None:
            return []
        user_id = user_id[0]
        data = self.repository.get_user_rooms(user_id)
        for i in range(len(data)):
            data[i] = {
                "id": data[i][0],
                "name": data[i][1]
            }
        return data

    def delete_room(self, room: RoomID):
        self.repository.delete_room(room.id)

    def update_room(self, room: RoomItem) -> bool:
        room_id = self.repository.get_room_id(room.id)
        if room_id is None:
            return False
        self.repository.update_room(room)
        return True
