from fastapi import APIRouter, Depends, HTTPException, status, Request, Response, Form
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import logging
from datetime import datetime, timedelta

import httpx # For async http requests
import json
import jwt # For JWT encoding/decoding

from app.core.config import settings
from app.core.db import get_user_profile, upsert_user_profile, get_user_profile_by_google_id

router = APIRouter()
logger = logging.getLogger(__name__)

# --- Google OAuth2 Configuration ---
GOOGLE_AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"
GOOGLE_REDIRECT_URI = settings.GOOGLE_REDIRECT_URI # Must be configured in Google Cloud Console
GOOGLE_SCOPES = "openid email profile" # Standard scopes for Google OAuth

# --- Token Management (for session) ---
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Short-lived for security, refresh using refresh token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token") # Placeholder token endpoint


# Helper to create/read session tokens
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    return {"id": user_id, "google_id": payload.get("google_id"), "email": payload.get("email")}

# --- Pydantic Models ---
class UserProfileData(BaseModel):
    programming_skill_level: Optional[str] = None
    robotics_experience: Optional[str] = None
    hardware_access: Optional[str] = None
    preferred_language: Optional[str] = None

class User(BaseModel):
    id: uuid.UUID
    google_id: str
    email: str
    profile: Optional[UserProfileData] = None

# --- Auth Endpoints ---

@router.get("/v1/auth/google/login", summary="Redirect to Google login page")
async def login_google(request: Request):
    """
    Initiates the Google OAuth2 login flow by redirecting the user to Google's
    authorization endpoint.
    """
    # Generate a secure state parameter to prevent CSRF
    state = str(uuid.uuid4())
    
    authorization_url = (
        f"{GOOGLE_AUTHORIZATION_URL}?"
        f"response_type=code&"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"scope={GOOGLE_SCOPES}&"
        f"redirect_uri={GOOGLE_REDIRECT_URI}&"
        f"state={state}&"
        f"access_type=offline&" # To get a refresh token
        f"prompt=consent" # To ensure refresh token is always returned
    )
    
    response = RedirectResponse(authorization_url)
    response.set_cookie(key="oauth_state", value=state, httponly=True, max_age=300) # 5 minutes expiry
    return response

@router.get("/v1/auth/google/callback", summary="Handle Google OAuth2 callback")
async def auth_callback_google(request: Request, response: Response, code: str, state: str):
    """
    Handles the redirect from Google after user authentication.
    Exchanges the authorization code for tokens and creates/updates user profile.
    """
    # Validate state to prevent CSRF attacks
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid state parameter")

    try:
        # Exchange authorization code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }
            )
            token_response.raise_for_status()
            token_data = token_response.json()
            access_token = token_data["access_token"]
            # Optional: store refresh_token if 'access_type=offline' was used

        # Fetch user info using the access token
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            userinfo_response.raise_for_status()
            user_info = userinfo_response.json()
        
        # Extract user details
        user_email = user_info.get("email")
        google_id = user_info.get("sub") # 'sub' is Google's unique user ID
        
        if not user_email or not google_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient user info from Google")

        # --- User Profile Creation/Update ---
        # Upsert user profile in our DB
        user_db_id = upsert_user_profile(google_id=google_id, email=user_email)
        
        if not user_db_id:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create or retrieve user profile")
        
        # Create access token for our internal session
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        internal_access_token = create_access_token(
            data={"sub": str(user_db_id), "google_id": google_id, "email": user_email}, 
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend dashboard or home, passing token in cookie
        response_redirect = RedirectResponse(url="/") # Redirect to frontend home
        response_redirect.set_cookie(
            key="access_token", 
            value=f"Bearer {internal_access_token}", 
            httponly=True, 
            max_age=access_token_expires.total_seconds(),
            samesite="Lax", # Important for security
            secure=settings.HTTPS_ENABLED # Use HTTPS_ENABLED from settings
        )
        response_redirect.delete_cookie("oauth_state") # Clean up state cookie
        return response_redirect

    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error during Google OAuth2 flow: {e.response.text}", exc_info=True)
        raise HTTPException(status_code=e.response.status_code, detail="Google OAuth2 token or userinfo error")
    except Exception as e:
        logger.error(f"Error during Google OAuth2 callback: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Authentication failed")

@router.get("/v1/auth/me", response_model=User, summary="Get current authenticated user's profile")
async def read_users_me(current_user: Dict = Depends(get_current_user)):
    """
    Retrieves the detailed profile of the currently authenticated user.
    """
    user_id = uuid.UUID(current_user["id"])
    google_id = current_user["google_id"]
    email = current_user["email"]

    db_user_profile = get_user_profile(user_id=user_id)
    if not db_user_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User profile not found in DB")
    
    return User(
        id=user_id,
        google_id=google_id,
        email=email,
        profile=UserProfileData(**db_user_profile)
    )

@router.post("/v1/auth/logout", summary="Logout user and clear session")
async def logout(response: Response):
    """
    Clears the user's session cookie to log them out.
    """
    response.delete_cookie(key="access_token", samesite="Lax", secure=settings.HTTPS_ENABLED)
    return {"message": "Logged out successfully"}

@router.post("/v1/user/profile", summary="Update user profiling data", response_model=User)
async def update_user_profile_data(
    profile_data: UserProfileData,
    current_user: Dict = Depends(get_current_user)
):
    """
    Allows a logged-in user to update their profiling data.
    """
    user_db_id = uuid.UUID(current_user["id"])
    google_id = current_user["google_id"]
    email = current_user["email"]

    updated_user_id = upsert_user_profile(
        google_id=google_id,
        email=email,
        programming_skill_level=profile_data.programming_skill_level,
        robotics_experience=profile_data.robotics_experience,
        hardware_access=profile_data.hardware_access,
        preferred_language=profile_data.preferred_language,
    )
    
    if not updated_user_id:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update user profile")

    # Fetch updated user details to return
    user_details = get_user_profile(user_id=user_db_id)
    return User(
        id=user_db_id,
        google_id=google_id,
        email=email,
        profile=UserProfileData(**user_details)
    )