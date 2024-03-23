from fastapi import APIRouter, Depends, Request
from starlette.responses import JSONResponse

from depends import get_user_service
from schemas.users import User, UserEmail, UserValidate, UserUpdate
from services.users import UserService
from utils.email_sender import send_verification_code

from random import randint

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/validate_email")
async def validate_email(user: UserEmail, user_service: UserService = Depends(get_user_service)):
    if user_service.validate_email(user.e_mail):
        return JSONResponse(status_code=400, content={"message": "Email already used"})
    verification_code = randint(100000, 999999)
    result = send_verification_code(user.e_mail, verification_code)
    if result == 0:
        return JSONResponse(status_code=200, content={"code": f"{verification_code}"})
    else:
        return JSONResponse(status_code=502, content={"message": "Invalid email"})


@router.post("/register")
async def register(user: User, user_service: UserService = Depends(get_user_service)):
    return JSONResponse(status_code=201, content={"token": user_service.create_user(user)})


@router.post("/authorize")
async def authorize(user: UserValidate, user_service: UserService = Depends(get_user_service)):
    token = user_service.validate_user(user)
    if token != '':
        return JSONResponse(status_code=200, content={"token": token})
    else:
        return JSONResponse(status_code=401, content={"message": "Not Authorized"})


@router.delete("/delete")
async def delete(request: Request, user_service: UserService = Depends(get_user_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if user_service.delete_user(token):
        return JSONResponse(status_code=200, content={"message": "Deleted"})
    else:
        return JSONResponse(status_code=401, content={"message": "Wrong token"})


@router.put("/update")
async def update(request: Request, user: UserUpdate, user_service: UserService = Depends(get_user_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    if user_service.update_user(user, token):
        return JSONResponse(status_code=200, content={"message": "Updated"})
    else:
        return JSONResponse(status_code=401, content={"message": "Wrong token"})


@router.get("/user_info")
async def user_info(request: Request, user_service: UserService = Depends(get_user_service)):
    token = request.headers.get('Authorization', None)
    if token is None:
        return JSONResponse(status_code=401, content={"message": "Not found token"})
    data = user_service.get_user(token)
    if data == {}:
        return JSONResponse(status_code=404, content={"message": "Not found"})
    else:
        return JSONResponse(status_code=200, content=data)
