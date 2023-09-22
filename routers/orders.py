from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/")
async def orders_list(request: Request):
    orders = list(request.app.database["orders"].find({"username": request.cookies.get("username")}, limit=100))
    return templates.TemplateResponse("orders.html", {"request": request, "orders": orders})
