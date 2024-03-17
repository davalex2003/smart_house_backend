from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_room_service, get_user_service
from schemas.rooms import Room, RoomDTO
from services.rooms import RoomService
from schemas.users import UserValidate

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/create")
async def create(room: Room, room_service: RoomService = Depends(get_room_service)):
    if room_service.create_room(room):
        return JSONResponse(status_code=201, content={"message": "Created"})
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})


@router.get("/get_rooms")
async def get_rooms(user: UserValidate, room_service: RoomService = Depends(get_room_service)):
    return room_service.get_rooms(user)
