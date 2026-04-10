<<<<<<< HEAD
import logging
import traceback

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import BadRequestError, InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
=======
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from app.schemas.auth import LoginRequest, RegisterRequest
>>>>>>> e9df211 (initial commit)
from app.schemas.common import MessageSchema
from app.schemas.token import RefreshTokenRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
<<<<<<< HEAD
logger = logging.getLogger(__name__)


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> RegisterResponse:
    service = AuthService(db)
    try:
        return service.register(payload)
    except BadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
=======


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    try:
        return service.register(payload)
>>>>>>> e9df211 (initial commit)
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


<<<<<<< HEAD
@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Log in with login and password",
    description="In Swagger OAuth2 password flow, put your account login into the username field.",
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> LoginResponse:
    service = AuthService(db)
    payload = LoginRequest(login=form_data.username, password=form_data.password)
    try:
        return service.login(payload)
    except BadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception("Unexpected error during login for login=%s", form_data.username)
        traceback.print_exc()
        raise exc


@router.post("/refresh", response_model=Token)
async def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> Token:
=======
@router.post("/login", response_model=Token)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    try:
        return service.login(payload)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> Token:
>>>>>>> e9df211 (initial commit)
    service = AuthService(db)
    try:
        return service.refresh(payload.refresh_token)
    except TokenInvalidError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/logout", response_model=MessageSchema)
<<<<<<< HEAD
async def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> MessageSchema:
=======
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> MessageSchema:
>>>>>>> e9df211 (initial commit)
    service = AuthService(db)
    service.revoke_refresh_token(payload.refresh_token)
    return MessageSchema(message="Logged out successfully")
