from typing import Annotated, List
from fastapi import APIRouter, Request, Form, Response, Body, status, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import User, UserResponse, UserUpdate
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def users_list(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    return users


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(request: Request, user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = request.app.database["users"].insert_one(user)
    created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})
    return created_user


@router.post("/register/form", response_class=RedirectResponse, status_code=302)
async def form(username: Annotated[str, Form()], email: Annotated[str, Form()], password: Annotated[str, Form()],
               response: Response, request: Request):
    response.set_cookie(key="username", value=username)
    request.app.database["users"].insert_one({'username': username, "email": email, "password": password})
    return "/"


@router.put("/{username}", response_model=UserResponse)
async def update_user(username: str, request: Request, user: UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["users"].update_one({"username": username}, {"$set": user})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"For user {username} nothing changed")
    if (existing_user := request.app.database["users"].find_one({"username": username})) is not None:
        return existing_user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found")


@router.delete("/{username}")
async def delete_item(username: str, request: Request, response: Response):
    delete_result = request.app.database["users"].delete_one({"username": username})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {username} not found")


@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=RedirectResponse, status_code=302)
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()], response: Response):
    response.set_cookie(key="username", value=username)
    return "/"


@router.get("/logout", response_class=RedirectResponse, status_code=302)
async def logout(response: Response):
    response.delete_cookie(key="username")
    return "/"
