from pydantic import BaseModel


class User(BaseModel):
    e_mail: str
    name: str
    surname: str
    hash_password: str


class UserEmail(BaseModel):
    e_mail: str


class UserValidate(BaseModel):
    e_mail: str
    hash_password: str


class UserUpdate(BaseModel):
    e_mail: str
    name: str
    surname: str
