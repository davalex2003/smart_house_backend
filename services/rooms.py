from typing import List

from repositories.rooms import RoomRepository
from schemas.rooms import RoomDTO, Room, RoomItem
from utils.jwt_worker import decode_data


class RoomService:

    def __init__(self, repository: RoomRepository):
        self.repository = repository

    def create_room(self, room: Room, token: str) -> tuple[bool, int]:
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False, 0
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
        if user_id is None:
            return False, 0
        user_id = user_id[0]
        room_dto = RoomDTO(name=room.name, user_id=user_id)
        self.repository.create_room(room_dto)
        room_id = self.repository.get_last_id()
        return True, room_id

    def get_rooms(self, token: str) -> List[RoomItem]:
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return []
        user_id = self.repository.get_user_id(data['e_mail'], data['hash_password'])
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

    def delete_room(self, room_id: int, token: str):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        self.repository.delete_room(room_id)
        return True

    def update_room(self, room: RoomItem, token: str) -> bool:
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return False
        room_id = self.repository.get_room_id(room.id)
        if room_id is None:
            return False
        self.repository.update_room(room)
        return True

    def get_room_devices(self, token: str, room_id):
        data = decode_data(token)
        if 'e_mail' not in data or 'hash_password' not in data:
            return []
        data = self.repository.get_room_devices(room_id)
        for i in range(len(data)):
            data[i] = {
                "device_id": data[i][0],
                "name": data[i][3],
                "type": data[i][4],
                "state": data[i][5],
                "ip": data[i][6],
                "time": data[i][7],
                "alarm_time": data[i][8],
                "alarm_lamp": data[i][9]
            }
        return data
