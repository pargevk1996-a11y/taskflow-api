from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_login_form
from app.core.exceptions import BadRequestError, InvalidCredentialsError, TokenInvalidError, UserAlreadyExistsError
from app.schemas.auth import LoginRequest, RegisterRequest
from app.schemas.common import MessageSchema
from app.schemas.token import RefreshTokenRequest, Token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    try:
        return service.register(payload)
    except BadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.post("/login", response_model=MessageSchema)
def login(payload: LoginRequest = Depends(get_login_form), db: Session = Depends(get_db)) -> MessageSchema:
    service = AuthService(db)
    try:
        service.login(payload)
        return MessageSchema(message="Welcome dude!")
    except BadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/token", response_model=Token, include_in_schema=False)
def issue_token(payload: LoginRequest = Depends(get_login_form), db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    try:
        return service.issue_token(payload)
    except BadRequestError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/refresh", response_model=Token)
def refresh(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> Token:
    service = AuthService(db)
    try:
        return service.refresh(payload.refresh_token)
    except TokenInvalidError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc


@router.post("/logout", response_model=MessageSchema)
def logout(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> MessageSchema:
    service = AuthService(db)
    service.revoke_refresh_token(payload.refresh_token)
    return MessageSchema(message="Logged out successfully")
