from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from bson import ObjectId
from models import Item
from routers import orders
from datetime import datetime

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_model=List[Item])
def items_list(request: Request):
    items = list(request.app.database["items"].find(limit=100))
    return items


@router.get("/{id}", response_class=HTMLResponse, response_model=Item)
async def find_item(id: str, request: Request):
    if (item := request.app.database["items"].find_one({"_id": ObjectId(id)})) is not None:
        return templates.TemplateResponse("update.html", {"request": request, "item": item})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")


@router.post("/", response_model=Item, status_code=201)
async def create_item(request: Request, item: Item = Body(...)):
    item = jsonable_encoder(item)
    new_item = request.app.database["items"].insert_one(item)
    created_item = request.app.database["items"].find_one({"_id": new_item.inserted_id})
    return created_item


@router.post("/{id}", response_class=RedirectResponse, status_code=302)
async def do_order_item(id: str, request: Request):
    if username := request.cookies.get("username"):
        request.app.database["orders"].insert_one({"item_id": id,
                                                   "username": username,
                                                   # "time": datetime.now(),
                                                   })
        return "/"
    return "/users/login"


@router.put("/{id}", response_model=Item)
async def update_item(id: str, request: Request, item: Item = Body(...)):
    item = {k: v for k, v in item.dict().items() if v is not None}
    if len(item) >= 1:
        update_result = request.app.database["items"].update_one({"_id": ObjectId(id)}, {"$set": item})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Item with ID {id} nothing changed")
    if (existing_item := request.app.database["items"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_item
    raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")


@router.delete("/{id}")
async def delete_item(id: str, request: Request, response: Response):
    delete_result = request.app.database["items"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")
