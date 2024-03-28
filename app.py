from fastapi import FastAPI, UploadFile, File, Request
from starlette.responses import JSONResponse

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
async def raspberry(file: UploadFile = File(...)):
    with open(file.filename, "wb") as f:
        f.write(await file.read())
    await notify_clients()
    return JSONResponse(content={"message": "Photo uploaded successfully"})


async def notify_clients():
    for client in connected_clients:
        try:
            await client.send_json({"message": "Alarm!"})
        except Exception as e:
            continue


@app.websocket("/security/client")
async def websocket_endpoint(websocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        connected_clients.remove(websocket)


@app.get("/security/photo")
async def photo(request: Request):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
