from fastapi import FastAPI, UploadFile, File, Request, WebSocket
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse
from starlette.websockets import WebSocketDisconnect

from routing.users import router as users_router
from routing.rooms import router as rooms_router
from routing.devices import router as devices_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = []

app.include_router(users_router)
app.include_router(rooms_router)
app.include_router(devices_router)


class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append({"ws": websocket, "ip": ""})

    def set_ip(self, websocket: WebSocket, ip: str):
        for i in self.active_connections:
            if i["ws"] == websocket:
                i["ip"] = ip

    def disconnect(self, websocket: WebSocket):
        old = self.active_connections
        self.active_connections = []
        for i in old:
            if i["ws"] != websocket:
                self.active_connections.append(i)

    async def broadcast(self, message: str, ip: str):
        for connection in self.active_connections:
            if ip == connection["ip"]:
                await connection["ws"].send_text(message)
                print(message)


manager = ConnectionManager()


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
    await manager.broadcast(ip, ip)
    with open(f"{ip}.png", "wb") as f:
        f.write(contents)
        f.close()
    return JSONResponse(content={"message": "Image received"})


@app.websocket("/security/client")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            manager.set_ip(websocket, ip=message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/security/photo")
async def photo(ip: str):
    return FileResponse(f"{ip}.png")
