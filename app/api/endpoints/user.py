from typing import List, Union
from fastapi import APIRouter, HTTPException
import app.crud.user as user_crud
import app.schemas.user_schema as user_schema

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/", response_model=List[user_schema.User])
async def get_users():
    result = user_crud.get_users()
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/", response_model=user_schema.User, status_code=201)
async def create_user(user: user_schema.User):
    result = user_crud.create_user(user)
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.get("/{user_id}", response_model=Union[user_schema.User, dict], status_code=200)
async def get_user(user_id: str):
    result = user_crud.get_user(user_id)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "Invalid ID":
            raise HTTPException(status_code=400, detail=result["error"])
        if result["error"] == "User not found":
            raise HTTPException(status_code=404, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.put("/{user_id}", response_model=user_schema.User, status_code=200)
async def update_user(user_id: str, user: user_schema.User):
    result = user_crud.update_user(user_id, user)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "Invalid ID":
            raise HTTPException(status_code=400, detail=result["error"])
        if result["error"] == "User not found":
            raise HTTPException(status_code=404, detail=result["error"])
        if result["error"] == "No changes made to the user":
            raise HTTPException(status_code=304, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: str):
    result = user_crud.delete_user(user_id)
    if isinstance(result, dict) and "error" in result:
        if result["error"] == "Invalid ID":
            raise HTTPException(status_code=400, detail=result["error"])
        if result["error"] == "User not found":
            raise HTTPException(status_code=404, detail=result["error"])
        raise HTTPException(status_code=500, detail=result["error"])
    return result
