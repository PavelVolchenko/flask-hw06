from fastapi import FastAPI
from fastapi.testclient import TestClient
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as item_router

app = FastAPI()
config = dotenv_values(".env")
app.include_router(item_router, tags=["items"], prefix="/item")

@app.on_event("startup")
async def startup_event():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"] + "test"]

@app.on_event("shutdown")
async def shutdown_event():
    app.mongodb_client.close()
    app.database.drop_collection("items")

def test_create_item():
    with TestClient(app) as client:
        response = client.post("/item/", json={"title": "Don Quixote", "description": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 201

        body = response.json()
        assert body.get("title") == "Don Quixote"
        assert body.get("description") == "Miguel de Cervantes"
        assert body.get("synopsis") == "..."
        assert "_id" in body


def test_create_item_missing_title():
    with TestClient(app) as client:
        response = client.post("/item/", json={"description": "Miguel de Cervantes", "synopsis": "..."})
        assert response.status_code == 422


def test_create_item_missing_author():
    with TestClient(app) as client:
        response = client.post("/item/", json={"title": "Don Quixote", "synopsis": "..."})
        assert response.status_code == 422


def test_create_item_missing_synopsis():
    with TestClient(app) as client:
        response = client.post("/item/", json={"title": "Don Quixote", "description": "Miguel de Cervantes"})
        assert response.status_code == 422


def test_get_item():
    with TestClient(app) as client:
        new_book = client.post("/item/", json={"title": "Don Quixote", "description": "Miguel de Cervantes", "synopsis": "..."}).json()

        get_book_response = client.get("/item/" + new_book.get("_id"))
        assert get_book_response.status_code == 200
        assert get_book_response.json() == new_book


def test_get_item_unexisting():
    with TestClient(app) as client:
        get_book_response = client.get("/item/unexisting_id")
        assert get_book_response.status_code == 404


def test_update_item():
    with TestClient(app) as client:
        new_book = client.post("/item/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        response = client.put("/item/" + new_book.get("_id"), json={"title": "Don Quixote 1"})
        assert response.status_code == 200
        assert response.json().get("title") == "Don Quixote 1"


def test_update_item_unexisting():
    with TestClient(app) as client:
        update_item_response = client.put("/item/unexisting_id", json={"title": "Don Quixote 1"})
        assert update_item_response.status_code == 404


def test_delete_item():
    with TestClient(app) as client:
        new_item = client.post("/item/", json={"title": "Don Quixote", "author": "Miguel de Cervantes", "synopsis": "..."}).json()

        delete_item_response = client.delete("/item/" + new_item.get("_id"))
        assert delete_item_response.status_code == 204


def test_delete_item_unexisting():
    with TestClient(app) as client:
        delete_item_response = client.delete("/item/unexisting_id")
        assert delete_item_response.status_code == 404