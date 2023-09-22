from fastapi import APIRouter, Body, Request, Depends, Response, HTTPException, status, Cookie
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from bson import ObjectId
from models import Item, ItemUpdate, ItemResponse
from routers import orders
from dependencies import get_token_header
from datetime import datetime

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/",
            response_model=List[ItemResponse],
            response_class=HTMLResponse,
            )
async def list_item(request: Request):
    items = list(request.app.database["items"].find(limit=100))

    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@router.get("/{id}",
            response_model=ItemResponse,
            response_class=HTMLResponse,
            )
async def find_item(id: str,
                    request: Request,
                    ):
    if (item := request.app.database["items"].find_one({"_id": ObjectId(id)})) is not None:
        return templates.TemplateResponse("update.html", {"request": request, "item": item})

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Item with ID {id} not found",
                        )


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=ItemResponse,
             )
async def create_item(request: Request,
                      item: Item = Body(...),
                      ):
    item = jsonable_encoder(item)
    new_item = request.app.database["items"].insert_one(item)
    created_item = request.app.database["items"].find_one(
        {"_id": new_item.inserted_id}
    )

    return created_item


@router.post("/{id}",
             response_class=RedirectResponse,
             status_code=302,
             )
async def list_item(id: str,
                    request: Request,
                    ):
    request.app.database["orders"].insert_one(
        {
            "item_id": id,
            "username": request.cookies.get("username"),
            "time": datetime.now(),
        }
    )
    return "/"


@router.put("/{id}",
            response_model=ItemResponse,
            )
async def update_item(id: str,
                      request: Request,
                      item: ItemUpdate = Body(...),
                      ):
    item = {k: v for k, v in item.dict().items() if v is not None}

    if len(item) >= 1:
        update_result = request.app.database["items"].update_one(
            {"_id": ObjectId(id)}, {"$set": item}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Item with ID {id} nothing changed",
                                )

    if (
            existing_item := request.app.database["items"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return existing_item

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Item with ID {id} not found",
                        )


@router.delete("/{id}")
async def delete_item(id: str,
                      request: Request,
                      response: Response,
                      ):
    delete_result = request.app.database["items"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Item with ID {id} not found",
                        )
