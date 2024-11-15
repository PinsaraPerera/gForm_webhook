from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from datetime import datetime
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

# Helper for BSON ObjectId validation
PyObjectId = Annotated[str, BeforeValidator(str)]

class User(BaseModel):
    id: Optional[PyObjectId] = Field(default=None, alias="_id")  # MongoDB auto-generated ID
    name: str
    age: int
    email: str
    is_active: bool = False  # Default to not active
    is_deleted: bool = False  # Default to not deleted(soft delete)
    is_admin: bool = False  # Default to non-admin
    created_at: int = Field(default_factory=lambda: int(datetime.timestamp(datetime.now())))  # Creation timestamp

    model_config = ConfigDict(
        populate_by_name = True,
        arbitrary_types_allowed = True,
        json_schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "name": "John Doe",
                "age": 25,
                "email": "sample@gmail.com",
                "is_active": False,
                "is_deleted": False,
                "is_admin": False,
                "created_at": 1621320000
            }
        },
    )
