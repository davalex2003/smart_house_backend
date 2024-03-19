from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_device_service
from schemas.devices import DeviceCreate, DeviceUpdate, Led, ClockLamp, ClockTime, Alarm
from services.devices import DeviceService, DeviceDelete
from schemas.users import UserValidate

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/create")
async def create(device: DeviceCreate, device_service: DeviceService = Depends(get_device_service)):
    result = device_service.create_device(device)
    if result[0]:
        return JSONResponse(status_code=201, content={"message": "Created", "id": result[1]})
    else:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})


@router.get("/get_all")
async def get_all(user: UserValidate, device_service: DeviceService = Depends(get_device_service)):
    result = device_service.get_user_devices(user)
    if result == {}:
        return JSONResponse(status_code=404, content={"message": "Not found user"})
    else:
        return JSONResponse(status_code=200, content=result)


@router.delete("/delete")
async def delete(device: DeviceDelete, device_service: DeviceService = Depends(get_device_service)):
    if device_service.delete_device(device):
        return JSONResponse(status_code=200, content={"message": "Deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found user"})


@router.put("/update")
async def update(device: DeviceUpdate, device_service: DeviceService = Depends(get_device_service)):
    if device_service.update_device(device):
        return JSONResponse(status_code=200, content={"message": "Updated"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found user"})


@router.put("/manage_led")
async def manage_led(device: Led, device_service: DeviceService = Depends(get_device_service)):
    data = device_service.manage_led(device)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_clock_lamp")
async def manage_clock_lamp(device: ClockLamp, device_service: DeviceService = Depends(get_device_service)):
    data = device_service.manage_clock_lamp(device)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_clock_time")
async def manage_clock_time(device: ClockTime, device_service: DeviceService = Depends(get_device_service)):
    data = device_service.manage_clock_time(device)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_alarm")
async def manage_alarm(device: Alarm, device_service: DeviceService = Depends(get_device_service)):
    data = device_service.manage_alarm(device)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})
