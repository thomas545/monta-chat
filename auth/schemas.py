from typing import Optional, Type, Any, Tuple
from datetime import datetime, timezone
from bson import ObjectId
from pydantic import BaseModel, Field, field_serializer

USER_COLLECTION = "users"


class User(BaseModel):
    full_name: Optional[str] = None
    email: str
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return int(created_at.timestamp())

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return int(updated_at.timestamp())


class UserRequest(User):
    is_active: bool = True
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)


class UserResponse(BaseModel):
    id: Optional[str] = Field(alias="_id")
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    access_token: Optional[str] = None
