from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from depends import get_user_service
from schemas.users import User, UserEmail
from services.users import UserService
from utils.email_sender import send_verification_code

from random import randint

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/validate_email")
async def validate_email(user_email: UserEmail):
    verification_code = randint(100000, 999999)
    result = send_verification_code(user_email.e_mail, verification_code)
    if result == 0:
        return JSONResponse(status_code=200, content={"code": f"{verification_code}"})
    else:
        return JSONResponse(status_code=502, content={"message": "Invalid email"})
