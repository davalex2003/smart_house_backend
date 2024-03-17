from pydantic import BaseModel


class Room(BaseModel):
    e_mail: str
    hash_password: str
    name: str


class RoomDTO(BaseModel):
    name: str
    user_id: int


class RoomItem(BaseModel):
    id: int
    name: str
