from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from depends import get_device_service
from schemas.devices import DeviceCreate, DeviceUpdate, Led, ClockLamp, ClockTime, Alarm, Security
from services.devices import DeviceService

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/create")
async def create(request: Request, device: DeviceCreate, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    result = device_service.create_device(device, token)
    if result[0]:
        return JSONResponse(status_code=201, content={"message": "Created", "id": result[1]})
    else:
        return JSONResponse(status_code=400, content={"message": result[1]})


@router.get("/get_all")
async def get_all(request: Request, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    result = device_service.get_user_devices(token)
    if result == {}:
        return JSONResponse(status_code=404, content={"message": "Not found user"})
    else:
        return JSONResponse(status_code=200, content=result)


@router.delete("/delete")
async def delete(request: Request, device_id: int, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if device_service.delete_device(device_id, token):
        return JSONResponse(status_code=200, content={"message": "Deleted"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found user"})


@router.put("/update")
async def update(request: Request, device: DeviceUpdate, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if device_service.update_device(device, token):
        return JSONResponse(status_code=200, content={"message": "Updated"})
    else:
        return JSONResponse(status_code=404, content={"message": "Not found user"})


@router.put("/manage_led")
async def manage_led(request: Request, device: Led, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = device_service.manage_led(device, token)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_clock_lamp")
async def manage_clock_lamp(request: Request, device: ClockLamp,
                            device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = device_service.manage_clock_lamp(device, token)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_clock_time")
async def manage_clock_time(request: Request, device: ClockTime,
                            device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = device_service.manage_clock_time(device, token)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_alarm")
async def manage_alarm(request: Request, device: Alarm, device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = device_service.manage_alarm(device, token)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})


@router.put("/manage_security")
async def manage_security(request: Request, device: Security,
                          device_service: DeviceService = Depends(get_device_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = device_service.manage_security(device, token)
    if data[0]:
        return JSONResponse(status_code=200, content={"message": data[1]})
    else:
        return JSONResponse(status_code=404, content={"message": data[1]})
