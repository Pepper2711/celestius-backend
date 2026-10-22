from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

class RegistrationCreate(BaseModel):
    name: str
    email: EmailStr
    college_department: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: int
    name: str
    email: str
    college_department: Optional[str] = None
    registered_at: datetime

    class Config:
        from_attributes = True

class RegistrationListResponse(BaseModel):
    capacity: int
    total_registered: int
    seats_remaining: int
    data: List[RegistrationResponse]
