from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as items_router
from fastapi.staticfiles import StaticFiles


config = dotenv_values(".env")

app = FastAPI()
app.include_router(items_router, tags=["items"], prefix="/items")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()














# import uvicorn
# import logging
# from fastapi import FastAPI
# from modelsSQLite import db, items, metadata, engine, List, Item, ItemAdd
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# metadata.create_all(engine)
#
# app = FastAPI()
#
#
# @app.on_event("startup")
# async def startup():
#     await db.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await db.disconnect()
#
#
# @app.get("/fake_items/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = items.insert().values(
#             title=f"item-{i}",
#             description=f"desc-{i}",
#             price=i,
#             is_del=False,
#             created_time="None",
#             updated_time="None",
#         )
#         await db.execute(query)
#     return {'message': f'{count} fake items create'}
#
#
# @app.get("/items/", response_model=List[Item])
# async def read_items():
#     query = items.select()
#     return await db.fetch_all(query)
#
#
# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id: int):
#     query = items.select().where(items.c.item_id == item_id)
#     return await db.fetch_one(query)
#
#
# @app.post("/items/", response_model=Item)
# async def create_item(item: ItemAdd):
#     query = items.insert().values(
#         title=item.title,
#         description=item.description,
#         price=item.price,
#         is_del=item.is_del,
#     )
#     last_record_id = await db.execute(query)
#     return {**item.model_dump(), "item_id": last_record_id}
#
#
# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id: int, new_item: ItemAdd):
#     query = items.update().where(items.c.item_id == item_id).values(**new_item.model_dump())
#     await db.execute(query)
#     return {**new_item.model_dump(), "item_id": item_id}
#
#
# @app.delete("/items/{item_id}", response_model=Item)
# async def delete_item(item_id: int):
#     query = items.update().where(items.c.item_id == item_id).values(is_del=True)
#     await db.execute(query)
#     return {"item_id": item_id, "is_del": True}
#
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
