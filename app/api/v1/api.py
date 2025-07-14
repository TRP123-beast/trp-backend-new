from fastapi import APIRouter
from app.api.v1.endpoints import users, properties, page_load

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(page_load.router, prefix="/page_load", tags=["page_load"]) 