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
    id: Union[ObjectId, str, None] = Field(default_factory=PyObjectId, alias="_id")
    title: Union[str, None] = None
    description: Union[str, None] = None
    price: Union[int, None] = None
    is_del: Union[bool, None] = False

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


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    password: Union[str, None] = None

    # class Config:
    #     populate_by_name = True
    #     arbitrary_types_allowed = True


# class UserResponse(BaseModel):
#     id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
#     username: str
#     email: str
#     password: str
#
#     class Config:
#         populate_by_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#
#
# class UserUpdate(BaseModel):
#     username: Optional[str] = None
#     email: Optional[str] = None
#     password: Optional[str] = None


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
