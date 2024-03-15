from pydantic import BaseModel


class User(BaseModel):
    id: int
    e_mail: str
    name: str
    surname: str
    hash_password: str


class UserEmail(BaseModel):
    e_mail: str
