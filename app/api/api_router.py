from fastapi import APIRouter

from app.api import api_messages
from app.api.endpoints import auth, users, client, admin, superuser, diagnostic, mechanic

auth_router = APIRouter()
auth_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router = APIRouter(
    responses={
        401: {
            "description": "No `Authorization` access token header, token is invalid or user removed",
            "content": {
                "application/json": {
                    "examples": {
                        "not authenticated": {
                            "summary": "No authorization token header",
                            "value": {"detail": "Not authenticated"},
                        },
                        "invalid token": {
                            "summary": "Token validation failed, decode failed, it may be expired or malformed",
                            "value": {"detail": "Token invalid: {detailed error msg}"},
                        },
                        "removed user": {
                            "summary": api_messages.JWT_ERROR_USER_REMOVED,
                            "value": {"detail": api_messages.JWT_ERROR_USER_REMOVED},
                        },
                    }
                }
            },
        },
    }
)
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(client.router, prefix="/client", tags=["client"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(auth.router, prefix="/superadmin", tags=["superadmin"])
api_router.include_router(superuser.router, prefix="/superuser", tags=["superuser"])
api_router.include_router(diagnostic.router, prefix="/diagnostic", tags=["diagnostic"])
api_router.include_router(mechanic.router, prefix="/mechanic", tags=["mechanic"])