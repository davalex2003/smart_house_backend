from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_user_service
from schemas.users import User, UserEmail, UserValidate
from services.users import UserService
from utils.email_sender import send_verification_code

from random import randint

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/validate_email")
async def validate_email(user_email: UserEmail, user_service: UserService = Depends(get_user_service)):
    if user_service.validate_email(user_email.e_mail):
        return JSONResponse(status_code=400, content={"message": "Email already used"})
    verification_code = randint(100000, 999999)
    result = send_verification_code(user_email.e_mail, verification_code)
    if result == 0:
        return JSONResponse(status_code=200, content={"code": f"{verification_code}"})
    else:
        return JSONResponse(status_code=502, content={"message": "Invalid email"})


@router.post("/register")
async def register(user: User, user_service: UserService = Depends(get_user_service)):
    user_service.create_user(user)
    return JSONResponse(status_code=201, content={"message": "Created"})


@router.post("/authorize")
async def authorize(user: UserValidate, user_service: UserService = Depends(get_user_service)):
    if user_service.validate_user(user):
        return JSONResponse(status_code=200, content={"message": "Authorized"})
    else:
        return JSONResponse(status_code=401, content={"message": "Not Authorized"})
