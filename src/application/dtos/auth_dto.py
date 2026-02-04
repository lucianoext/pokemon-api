from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegistrationDTO(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Username único")
    email: EmailStr = Field(description="Email válido")
    password: str = Field(
        min_length=6, max_length=100, description="Contraseña mínimo 6 caracteres"
    )
    trainer_name: str | None = Field(
        default=None, max_length=100, description="Nombre del entrenador (opcional)"
    )
    trainer_gender: str | None = Field(
        default=None, max_length=10, description="Género del entrenador"
    )
    trainer_region: str | None = Field(
        default=None, max_length=20, description="Región del entrenador"
    )


class UserLoginDTO(BaseModel):
    username: str = Field(description="Username o email")
    password: str = Field(description="Contraseña")


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Tiempo de expiración en segundos")


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(description="Token de refresh")


class UserResponseDTO(BaseModel):
    id: int | None
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    trainer_id: int | None = None

    class Config:
        from_attributes = True


class UserWithTrainerDTO(BaseModel):
    id: int | None
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    trainer: "TrainerBasicDTO | None" = None

    class Config:
        from_attributes = True


class TrainerBasicDTO(BaseModel):
    id: int | None
    name: str
    gender: str
    region: str

    class Config:
        from_attributes = True


class ChangePasswordDTO(BaseModel):
    current_password: str = Field(description="Contraseña actual")
    new_password: str = Field(
        min_length=6, max_length=100, description="Nueva contraseña"
    )


class UpdateUserDTO(BaseModel):
    email: EmailStr | None = None
    is_active: bool | None = None


class ResetPasswordDTO(BaseModel):
    email: EmailStr = Field(description="Email del usuario")


class MessageResponseDTO(BaseModel):
    message: str


class LoginResponseDTO(BaseModel):
    user: UserResponseDTO
    tokens: TokenResponseDTO
    message: str = "Login successful"

    class Config:
        from_attributes = True
