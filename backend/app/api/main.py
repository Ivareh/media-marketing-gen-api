from fastapi import APIRouter, Security

from app.api.routes import chat_logs, chat_sessions, tenants, users, utils
from app.core.security import azure_scheme

api_router = APIRouter()
api_router.include_router(tenants.router, dependencies=[Security(azure_scheme)])
api_router.include_router(users.router, dependencies=[Security(azure_scheme)])
api_router.include_router(chat_sessions.router, dependencies=[Security(azure_scheme)])
api_router.include_router(chat_logs.router, dependencies=[Security(azure_scheme)])
api_router.include_router(utils.router)
