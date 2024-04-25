from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from .services import create_user, get_user
from .schemas import User, UserResponse, UserRequest
from .utils import create_access_token, verify_password


load_dotenv()

users_routers = APIRouter(prefix="/users/auth", tags=["auth"])


@users_routers.post("/signup/", response_model=UserResponse)
async def signup(req: UserRequest):
    if get_user({"email": req.email}):
        raise HTTPException(400, "User Already exists")

    try:
        user_json = req.model_dump()
        user_id = create_user(user_json)
        user_json["_id"] = user_id
        user_json["access_token"] = create_access_token(user_json)
    except  Exception as exc:
        raise HTTPException(400, exc.args)

    return UserResponse(**user_json)


@users_routers.post("/login/", response_model=UserResponse)
async def login(
    user: User,
):
    email = user.email
    password = user.password
    db_user = get_user({"email": email})

    if not db_user or not verify_password(password, db_user.get("password")):
        raise HTTPException(403, "Invalid User")
    
    if  not db_user.get("is_active"):
        raise HTTPException(401, "Account is inactive")

    db_user["access_token"] = create_access_token(db_user)
    return db_user
