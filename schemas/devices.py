from pydantic import BaseModel
from typing import Optional


class DeviceCreate(BaseModel):
    e_mail: str
    hash_password: str
    room_id: int
    name: str
    type: str
    ip: str


class DeviceItem(BaseModel):
    name: str
    type: str
    state: bool
    time: Optional[str]
    alarm_time: Optional[str]
    alarm_lamp: bool


class DeviceDelete(BaseModel):
    e_mail: str
    hash_password: str
    device_id: int


class DeviceUpdate(BaseModel):
    e_mail: str
    hash_password: str
    id: int
    room_id: int
    name: str
    type: str


class Led(BaseModel):
    id: int
    color: str
    state: bool


class ClockLamp(BaseModel):
    id: int
    state: bool


class ClockTime(BaseModel):
    id: int
    time: str


class Alarm(BaseModel):
    id: int
    state: bool
    time: str


class Security(BaseModel):
    id: int
    state: bool
