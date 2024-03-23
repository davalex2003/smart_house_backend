from pydantic import BaseModel
from typing import Optional


class DeviceCreate(BaseModel):
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


class DeviceUpdate(BaseModel):
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
