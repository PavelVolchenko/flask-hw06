import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Item(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    title: str = Field(default="Fill in title")
    description: str = Field(default="Fill in description")
    price: float = Field(default=0)
    is_del: bool = Field(default=False)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True

        json_schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Some Title Text About Item",
                "description": "A lot of text describable a some properties and characteristics abot item.",
                "price": 2500,
                "is_del": False,
            }
        }
#

class ItemUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    is_del: Optional[bool]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Some Title Text About Item",
                "description": "A lot of text describable a some properties and characteristics abot item.",
                "price": 2500,
                "is_del": False,
            }
        }
