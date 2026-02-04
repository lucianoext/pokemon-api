from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from src.application.dtos.auth_dto import (
    ChangePasswordDTO,
    LoginResponseDTO,
    MessageResponseDTO,
    UserLoginDTO,
    UserRegistrationDTO,
    UserResponseDTO,
)
from src.application.services.auth_service import AuthService
from src.domain.entities.user import User
from src.persistence.database import get_database
from src.persistence.repositories import SqlAlchemyUserRepository
from src.presentation.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])


def get_auth_service(db: Session = Depends(get_database)) -> AuthService:
    user_repository = SqlAlchemyUserRepository(db)
    return AuthService(user_repository)


@router.post(
    "/register", response_model=UserResponseDTO, status_code=HTTPStatus.CREATED
)
def register_user(
    user_data: UserRegistrationDTO, service: AuthService = Depends(get_auth_service)
) -> UserResponseDTO:
    try:
        return service.register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=LoginResponseDTO)
def login_user(
    login_data: UserLoginDTO, service: AuthService = Depends(get_auth_service)
) -> LoginResponseDTO:
    try:
        return service.authenticate_user(login_data)
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))


@router.get("/me", response_model=UserResponseDTO)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user),
) -> UserResponseDTO:
    from datetime import datetime

    return UserResponseDTO(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at or datetime.utcnow(),
        trainer_id=current_user.trainer_id,
    )


@router.put("/change-password", response_model=MessageResponseDTO)
def change_password(
    password_data: ChangePasswordDTO,
    current_user: User = Depends(get_current_active_user),
    service: AuthService = Depends(get_auth_service),
) -> MessageResponseDTO:
    try:
        if current_user.id is None:
            raise ValueError("Invalid user ID")
        service.change_password(current_user.id, password_data)
        return MessageResponseDTO(message="Password changed successfully")
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
