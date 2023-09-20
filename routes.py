from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from typing import List
from bson import ObjectId

from models import Item, ItemUpdate, ItemResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/", response_description="Create a new item", status_code=status.HTTP_201_CREATED,
             response_model=ItemResponse)
def create_item(request: Request, item: Item = Body(...)):
    item = jsonable_encoder(item)
    new_item = request.app.database["items"].insert_one(item)
    created_item = request.app.database["items"].find_one(
        {"_id": new_item.inserted_id}
    )
    return created_item


@router.get("/", response_description="List all items", response_model=List[ItemResponse], response_class=HTMLResponse)
def list_item(request: Request):
    items = list(request.app.database["items"].find(limit=100))
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@router.get("/{id}", response_description="Get a single item by id", response_model=ItemResponse, response_class=HTMLResponse)
def find_item(id: str, request: Request):
    if (item := request.app.database["items"].find_one({"_id": ObjectId(id)})) is not None:
        return templates.TemplateResponse("update.html", {"request": request, "item": item})

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")


@router.put("/{id}", response_description="Update a item", response_model=ItemResponse, response_class=HTMLResponse)
def update_item(id: str, request: Request, item: ItemUpdate = Body(...)):
    item = {k: v for k, v in item.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = request.app.database["items"].update_one(
            {"_id": ObjectId(id)}, {"$set": item}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")

    if (
            existing_item := request.app.database["items"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return templates.TemplateResponse("update.html", {"request": request, "item": existing_item})
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")


@router.delete("/{id}", response_description="Delete a item")
def delete_item(id: str, request: Request, response: Response):
    delete_result = request.app.database["items"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item with ID {id} not found")
