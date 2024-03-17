from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_room_service
from schemas.rooms import Room, RoomDTO, RoomID, RoomItem
from services.rooms import RoomService
from schemas.users import UserValidate

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/create")
async def create(room: Room, room_service: RoomService = Depends(get_room_service)):
    result = room_service.create_room(room)
    if result[0]:
        return JSONResponse(status_code=201, content={"message": "Created", "id": result[1]})
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})


@router.get("/get_rooms")
async def get_rooms(user: UserValidate, room_service: RoomService = Depends(get_room_service)):
    return room_service.get_rooms(user)


@router.delete("/delete")
async def delete(room: RoomID, room_service: RoomService = Depends(get_room_service)):
    room_service.delete_room(room)
    return JSONResponse(status_code=200, content={"message": "Deleted"})


@router.put("/update")
async def update(room: RoomItem, room_service: RoomService = Depends(get_room_service)):
    if room_service.update_room(room):
        return JSONResponse(status_code=200, content={"message": "Updated"})
    else:
        return JSONResponse(status_code=404, content={"message": "No room with that id"})


@router.get("/get_devices")
async def get_devices(room: RoomID, room_service: RoomService = Depends(get_room_service)):
    return room_service.get_room_devices(room.id)
