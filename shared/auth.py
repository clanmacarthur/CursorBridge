"""JWT Authentication middleware for Supabase Auth."""

import os
from typing import Optional
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


def get_supabase_client():
    """Get Supabase client for auth validation."""
    from supabase import create_client
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set")
    
    return create_client(url, key)


async def validate_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """
    Validate Supabase JWT and return user info.
    
    Usage in endpoint:
        @app.get("/protected")
        async def protected_route(user: dict = Depends(validate_jwt)):
            return {"user_id": user["id"]}
    """
    if not credentials:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    token = credentials.credentials
    
    try:
        client = get_supabase_client()
        # Validate token with Supabase
        response = client.auth.get_user(token)
        
        if not response or not response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = response.user
        return {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "aud": user.aud,
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")


async def optional_jwt(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> Optional[dict]:
    """
    Optional JWT validation - returns None if no token provided.
    Useful for endpoints that work for both authenticated and anonymous users.
    """
    if not credentials:
        return None
    
    try:
        return await validate_jwt(credentials)
    except HTTPException:
        return None

