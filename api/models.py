from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Launchpad(BaseModel):
    id: str
    name: str
    region: str
    timezone: str
    latitude: float
    longitude: float
    status: str


class Rocket(BaseModel):
    id: str
    name: str
    active: bool
    type: str
    description: str


class Launch(BaseModel):
    id: str
    rocket: Rocket
    success: Optional[bool]
    details: Optional[str]
    launchpad: Launchpad
    date: datetime
