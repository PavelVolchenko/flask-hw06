from fastapi import APIRouter, Request, status, Cookie, Body, Response, HTTPException, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Order, Item
from datetime import datetime
from bson import ObjectId
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=RedirectResponse, response_model=List[Order], status_code=302)
async def orders(request: Request):
    if username := request.cookies.get("username"):
        orders = list(request.app.database["orders"].find({"username": username}, limit=100)).__reversed__()
        return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
    orders = list(request.app.database["orders"].find({}, limit=100))
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})


@router.get("/api", response_model=List[Order])
async def orders_api(request: Request):
    orders = list(request.app.database["orders"].find({}, limit=100))
    return orders


@router.post("/{id}", response_class=RedirectResponse, status_code=302)
async def order_create(id: str, request: Request):
    logger.debug("\nIncoming request to CREATE a new order")
    new_order = {
        "item_id": id,
        "username": request.cookies.get('username'),
        "time": datetime.now()
    }
    logger.debug(f"\nCreate new {type(new_order)} order: {new_order}")
    order = Order(**new_order)
    logger.debug(f"\nSubmit order to {type(order)}")
    request.app.database["orders"].insert_one(order.model_dump())
    logger.debug(f"\nRedirect to orders page {request.cookies.get('username')}")
    return "/orders"


@router.post("/", response_model=Order, status_code=201)
async def order_create_api(request: Request, order: Order = Body()):
    new_order = request.app.database["orders"].insert_one(order.model_dump())
    created_order = request.app.database["orders"].find_one({"_id": new_order.inserted_id})
    return created_order


@router.put("/{id}", response_model=Order)
async def order_update(id: str, request: Request, order: Order = Body(...)):
    order = {k: v for k, v in order.model_dump().items() if v is not None}
    if len(order) >= 1:
        update_result = request.app.database["orders"].update_one({"_id": ObjectId(id)}, {"$set": order})
        if update_result.modified_count == 0:
            raise HTTPException(status_code=404, detail=f"Order ID {id} nothing changed")
    if (existing_order := request.app.database["orders"].find_one({"_id": ObjectId(id)})) is not None:
        return existing_order
    raise HTTPException(status_code=404, detail=f"Order ID {id} not found")


@router.delete("/{id}")
async def order_delete(id: str, request: Request, response: Response):
    delete_result = request.app.database["orders"].delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order ID {id} not found")
