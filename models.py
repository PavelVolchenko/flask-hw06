from typing import Optional
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
    title: str = Field(default="Title")
    description: str = Field(default="Description")
    price: int = Field(default=0)
    is_del: bool = Field(default=False)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Title Item",
                "description": "Text describable about item.",
                "price": 2500,
                "is_del": 0,
            }
        }


class ItemResponse(Item):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")


# class ItemResponse(BaseModel):
#     id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
#     title: str = Field(default="Fill in title")
#     description: str = Field(default="Fill in description")
#     price: int = Field(default=0)
#
#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         json_schema_extra = {
#             "example": {
#                 "_id": "650ae2230d866b3c0390d626",
#                 "title": "Item",
#                 "description": "Describable item.",
#                 "price": 2500,
#             }
#         }


class ItemUpdate(Item):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None
    is_del: Optional[bool] = None


class User(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserResponse(BaseModel):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    password: str

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


class Order(BaseModel):
    username: str
    item_id: str

    # time: object = Field(default_factory=datetime.now)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class OrderResponse(Order):
    id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    # time: str | None


class OrderUpdate(OrderResponse):
    username: Optional[str] = None
    item_id: Optional[str] = None
    # time: Optional[object] = None
