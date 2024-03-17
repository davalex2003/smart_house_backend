from fastapi import FastAPI
from starlette.responses import JSONResponse

from routing.users import router as users_router
from routing.rooms import router as rooms_router

app = FastAPI()

app.include_router(users_router)
app.include_router(rooms_router)


@app.get("/ping")
async def ping():
    return JSONResponse(status_code=200, content={"message": "pong"})


@app.get("/")
async def root():
    return "Бэкенд для курсового проекта. Для документации вызовите /docs"
