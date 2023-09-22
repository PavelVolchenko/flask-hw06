from fastapi import APIRouter, Request, status, Cookie, Body, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models import OrderResponse, Order, OrderUpdate
from datetime import datetime

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/", response_class=RedirectResponse, response_model=List[OrderResponse], status_code=302)
async def orders(request: Request):
    if username := request.cookies.get("username"):
        orders = list(request.app.database["orders"].find({"username": username}, limit=100))
        return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
    orders = list(request.app.database["orders"].find({}, limit=100))
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})


@router.get("/api", response_model=List[OrderResponse])
async def orders_api(request: Request):
    orders = list(request.app.database["orders"].find({}, limit=100))
    return orders


@router.post("/")
async def order_create(request: Request, order: Order = Body(...)):
    order = jsonable_encoder(order)
    new_order = request.app.database["orders"].insert_one(order)
    created_order = request.app.database["orders"].find_one({"_id": new_order.inserted_id})
    return created_order

