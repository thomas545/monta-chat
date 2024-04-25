from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from .services import create_chat, get_chats_list
from .schemas import ChatResponse, ChatRequest
from auth.schemas import UserResponse
from auth.utils import get_current_active_user
from core.gemini import call_langchain_gemini


load_dotenv()

chats_routers = APIRouter(prefix="/chats", tags=["chats"])


@chats_routers.post("/ai/chat/", response_model=ChatResponse)
async def chat_api(
    chat: ChatRequest,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    chat.user_id = current_user.id
    response = call_langchain_gemini(chat.query)
    chat.response = response
    chat_id = create_chat(chat.model_dump())
    return ChatResponse(_id=chat_id, **chat.model_dump())


@chats_routers.get("/ai/chat/list/")
async def get_chat_list_api(
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
):
    chats = get_chats_list(current_user.id)
    return {"chats": chats, "count": len(chats)}
