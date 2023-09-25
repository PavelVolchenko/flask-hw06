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
    title: str
    description: str | None = None
    price: int
    id: ObjectId | str | None = Field(default_factory=PyObjectId, alias="_id")

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



class User(BaseModel):
    username: str
    email: str | None = None
    password: str | None = None
    id: ObjectId | str | None = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Order(BaseModel):
    item_id: str | None
    username: str | None
    id: ObjectId | str | None = Field(default_factory=PyObjectId, alias="_id")
    time: datetime | None = Field(default_factory=datetime.now)
    # time: datetime | None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        # {datetime: str}

# class OrderResponse(Order):
#     id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
#     # time: str | None
#
#
# class OrderUpdate(OrderResponse):
#     username: Optional[str] = None
#     item_id: Optional[str] = None
#     # time: Optional[object] = None
