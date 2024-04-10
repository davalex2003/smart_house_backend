from fastapi import FastAPI, UploadFile, File, Request
from starlette.responses import JSONResponse, FileResponse

from routing.users import router as users_router
from routing.rooms import router as rooms_router
from routing.devices import router as devices_router

app = FastAPI()

connected_clients = []

app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(devices_router)


@app.get("/ping")
async def ping():
    return JSONResponse(status_code=200, content={"message": "pong"})


@app.get("/")
async def root():
    return "Бэкенд для курсового проекта. Для документации вызовите /docs"


@app.post("/security/raspberry")
async def raspberry(request: Request, image: UploadFile = File(...)):
    contents = await image.read()
    ip = request.client.host
    with open(f"{ip}.png", "wb") as f:
        f.write(contents)
        f.close()
    await notify_clients(ip)
    return JSONResponse(content={"message": "Image received"})


async def notify_clients(ip: str):
    for client in connected_clients:
        if client['ip'] == ip:
            try:
                await client.send_json({"message": "Alarm!"})
            except Exception:
                continue


@app.websocket("/security/client")
async def websocket_endpoint(websocket):
    await websocket.accept()
    try:
        message = await websocket.receive_text()
        connected_clients.append({"websocket": websocket, "ip": message})
    except Exception:
        connected_clients.remove(websocket)


@app.get("/security/photo")
async def photo(ip: str):
    return FileResponse(f'{ip}.jpg')
