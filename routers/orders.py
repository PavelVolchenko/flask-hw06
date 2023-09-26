from fastapi import APIRouter, Request, status, Cookie, Body, Response, HTTPException, Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models import Order, Item
from datetime import datetime
from bson import ObjectId
import logging
import main

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
    }
    logger.debug(f"\nCreate new {type(new_order)} order: {new_order}")
    order = Order(**new_order)
    logger.debug(f"\nSubmit order to {type(order)}")
    request.app.database["orders"].insert_one(order.model_dump())
    logger.debug(f"\nRedirect to orders page {request.cookies.get('username')}")
    return "/orders"


#
#
# @router.post("/{order_id}{q}")
# async def order_delete(order_id: str, request: Request):
#     order_to_delete = {
#         "item_id": item_id,
#         "username": request.cookies.get('username'),
#     }
#     logger.debug(f"\nCreate new {type(new_order)} order: {new_order}")
#     order = Order(**new_order)
#     logger.debug(f"\nSubmit order to {type(order)}")
#     request.app.database["orders"].insert_one(order.model_dump())
#     logger.debug(f"\nRedirect to orders page {request.cookies.get('username')}")
#     return "/orders"




# @router.post("/")
# def delete_order():
#     with main.app as client:
#         new_order = client.post("/orders/", json={"item_id": "test insert", "username": "useragent"}).json()
#         logger.debug(msg=new_order)
#         delete_order_response = client.delete("/orders/" + new_order.get("_id"))
#         logger.debug(msg=new_order.get("_id"))
#         logger.debug(msg=delete_order_response)
#         assert delete_order_response.status_code == 204


# @router.post("/{item_id}",
#              # response_class=RedirectResponse,
#              # status_code=302,
#              response_model=Order,
#              )
# async def do_order(
#         *,
#         item_id: str = Path(title="The ID of the item to order"),
#         order: Order = Body(),
#         q: str | None = None,
#         request: Request,
# ):
#     logger.debug(msg=str(item_id))
#     order = order.model_dump(order)
#     order = (
#     # order = request.app.database["orders"].insert_one(
#     # request.app.database["orders"].insert_one(
#         {
#             "item_id": item_id,
#             "username": request.cookies.get("username"),
#             "time": datetime.now(),
#         }
#     )
#     order = request.app.database["orders"].insert_one(order.model_dump())
#     return order
#     # new_order = request.app.database["orders"].find_one({"_id": order.inserted_id})
#     # return templates.TemplateResponse("orders.html", {"request": request, "orders": new_order})
#
#
# @router.put("/{order_id}", response_model=Order)
# async def order_update(
#         *,
#         order_id: str = Path(title="The ID of the item order to change"),
#         request: Request,
#         # order: Order = Body(...),
#         order: Order,
# ):
#     order = {k: v for k, v in order.model_dump().items() if v is not None}
#     print("Кол-во параметров для обновления: ", len(order))
#     if len(order) >= 1:
#         update_result = request.app.database["orders"].update_one({"_id": order_id}, {"$set": order})
#         if update_result.modified_count == 0:
#             raise HTTPException(status_code=404, detail=f"Order ID {order_id} nothing changed")
#     if (existing_item := request.app.database["orders"].find_one({"_id": order_id})) is not None:
#         return existing_item
#     raise HTTPException(status_code=404, detail=f"Order ID {order_id} not found")
#
#
#
# @router.delete("/{id}")
# async def order_delete(
#         *,
#         id: str = Path(title="ID of the order to delete"),
#         q: str | None = None,
#         order: Order,
#         request: Request,
# ):
#     result = {"_id": id, **order.model_dump()}
#     print(**result)
#     if q:
#         result.update({"q": q})
#         return result
#         #
#         # delete_result = request.app.database["orders"].delete_one({"_id": id})
#         # if delete_result.deleted_count == 1:
#         #     response.status_code = status.HTTP_204_NO_CONTENT
#         #     return response
#         # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found")
#
# # @router.put("/{order_id}", response_class=RedirectResponse, response_model=Order)
# # async def order_update(order_id: str, request: Request, order: Order):
# #     order = jsonable_encoder(order)
# #     if (order := request.app.database["orders"].find_one({"_id": order.get("id")})) is not None:
# #         return templates.TemplateResponse("update.html", {"request": request, "order": order})
# #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order ID {order_id} not found")
