from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import user

app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI MongoDB example application!"}

