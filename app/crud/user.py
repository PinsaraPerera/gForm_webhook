from bson import ObjectId
from pymongo.collection import Collection
from app.schemas.user_schema import User
from app.db.db import db
from typing import Optional, List, Union

# Get the MongoDB collection for users
collection: Collection = db["users"]

def get_users() -> List[dict]:
    try:
        users = collection.find()  # Get all users
        return [{**user, "_id": str(user["_id"])} for user in users]
    except Exception as e:
        return {"error": f"Failed to retrieve users: {str(e)}"}

def create_user(user: User) -> Union[dict, str]:
    try:
        user_dict = user.model_dump(by_alias=True, exclude={"id"})  # Exclude the id field
        result = collection.insert_one(user_dict)  # Insert the user
        user_dict["_id"] = str(result.inserted_id)  # Attach the generated id to the user
        return user_dict
    except Exception as e:
        return {"error": f"Failed to create user: {str(e)}"}

def get_user(user_id: str) -> Union[dict, str]:
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid ID"}
    try:
        user = collection.find_one({"_id": ObjectId(user_id)})  # Get the user by id
        if user:
            return {**user, "_id": str(user["_id"])}
        return {"error": "User not found"}
    except Exception as e:
        return {"error": f"Failed to retrieve user: {str(e)}"}

def update_user(user_id: str, user: User) -> Union[dict, str]:
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid ID"}
    try:
        update_data = user.model_dump(by_alias=True, exclude={"id"}, exclude_unset=True)  # Exclude the id field
        result = collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})  # Update the user by id

        if result.matched_count == 0:
            return {"error": "User not found"}
        if result.modified_count == 0:
            return {"error": "No changes made to the user"}
        
        updated_user = collection.find_one({"_id": ObjectId(user_id)})  # Fetch updated user
        if updated_user:
            updated_user["_id"] = str(updated_user["_id"])
        return updated_user
    except Exception as e:
        return {"error": f"Failed to update user: {str(e)}"}

def delete_user(user_id: str) -> dict:
    if not ObjectId.is_valid(user_id):
        return {"error": "Invalid ID"}
    try:
        result = collection.delete_one({"_id": ObjectId(user_id)})  # Delete the user by id
        if result.deleted_count == 0:
            return {"error": "User not found"}
        return {"message": "User deleted successfully"}
    except Exception as e:
        return {"error": f"Failed to delete user: {str(e)}"}
