from typing import Optional, Type, Any, Tuple
from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_serializer


CHAT_COLLECTION = "chats"


class Chat(BaseModel):
    user_id: str = ""
    query: str
    response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return int(created_at.timestamp())

    @field_serializer("updated_at")
    def serialize_updated_at(self, updated_at: datetime, _info):
        return int(updated_at.timestamp())


class ChatRequest(Chat):
    user_id: Optional[str] = ""
    query: str
    response: Optional[str] = ""
    created_at: Optional[datetime] = datetime.now(timezone.utc)
    updated_at: Optional[datetime] = datetime.now(timezone.utc)


class ChatResponse(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: Optional[str]
    query: str
    response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ChatResponseList(BaseModel):
    id: Optional[str] = Field(alias="_id", default=None)
    user_id: Optional[str] = None
    query: Optional[str] = None
    response: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
