from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from services.rooms.depends import get_room_service
from schemas.rooms import Room, RoomItem
from services.rooms.services.rooms import RoomService

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/create")
async def create(room: Room, request: Request, room_service: RoomService = Depends(get_room_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    result = room_service.create_room(room, token)
    if result[0]:
        return JSONResponse(status_code=201, content={"message": "Created", "id": result[1]})
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})


@router.get("/list")
async def get_rooms(request: Request, room_service: RoomService = Depends(get_room_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    return room_service.get_rooms(token)


@router.delete("/delete")
async def delete(request: Request, room_id: int, room_service: RoomService = Depends(get_room_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if room_service.delete_room(room_id, token):
        return JSONResponse(status_code=200, content={"message": "Deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found"})


@router.put("/update")
async def update(request: Request, room: RoomItem, room_service: RoomService = Depends(get_room_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if room_service.update_room(room, token):
        return JSONResponse(status_code=200, content={"message": "Updated"})
    else:
        return JSONResponse(status_code=404, content={"message": "No room with that id"})


@router.get("/devices")
async def get_devices(room_id: int, request: Request, room_service: RoomService = Depends(get_room_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    return room_service.get_room_devices(token, room_id)
