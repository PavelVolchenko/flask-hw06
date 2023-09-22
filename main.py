from fastapi import FastAPI, Depends, Request, Cookie
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from routers import users, items, orders
from routers.items import list_items
from fastapi.templating import Jinja2Templates
from typing import List
from models import ItemResponse

config = dotenv_values(".env")
app = FastAPI()
app.include_router(users.router, tags=["users"], prefix="/users")
app.include_router(items.router, tags=["items"], prefix="/items")
app.include_router(orders.router, tags=["orders"], prefix="/orders")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse, response_model=List[ItemResponse])
async def index(request: Request):
    items = list_items(request)
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
