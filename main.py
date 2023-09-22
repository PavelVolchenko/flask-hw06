from fastapi import FastAPI, Depends, Request, Cookie
from dotenv import dotenv_values
from pymongo import MongoClient
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from routers import users, items, orders

config = dotenv_values(".env")
app = FastAPI()
app.include_router(users.router, tags=["users"], prefix="/users")
app.include_router(items.router, tags=["items"], prefix="/items")
app.include_router(orders.router, tags=["orders"], prefix="/orders")
app.mount("/static", StaticFiles(directory="static"), name="static")


# @app.middleware("http")
# async def add_cookies_header(request: Request,  call_next):
#     print("Middleware")
#     response = await call_next(request)
#     return response


@app.get("/", response_class=RedirectResponse, status_code=302)
async def index():
    return "/items"


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()
