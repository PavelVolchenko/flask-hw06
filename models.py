from typing import Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Item(BaseModel):
    title: str | None = None
    description: str | None = None
    price: int | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Title Item",
                "description": "Text describable",
                "price": 2500,
            }
        }


class ItemNew(Item):
    id: ObjectId | str | None = Field(default_factory=PyObjectId, alias="_id")


class User(BaseModel):
    username: str
    email: str | None = None
    password: str | None = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserNew(User):
    id: ObjectId | str | None = Field(default_factory=PyObjectId, alias="_id")


class Order(BaseModel):
    item_id: str | None = None
    username: str | None = None
    time: datetime | None = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
