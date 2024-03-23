from pydantic import BaseModel


class Room(BaseModel):
    name: str


class RoomDTO(BaseModel):
    name: str
    user_id: int


class RoomItem(BaseModel):
    id: int
    name: str
