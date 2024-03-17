from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_device_service
from schemas.devices import DeviceCreate
from services.devices import DeviceService
from schemas.users import UserValidate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/create")
async def create(device: DeviceCreate, device_service: DeviceService = Depends(get_device_service)):
    result = device_service.create_device(device)
    if result[0]:
        return JSONResponse(status_code=201, content={"message": "Created", "id": result[1]})
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})
