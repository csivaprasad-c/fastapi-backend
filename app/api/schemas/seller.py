from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.core.exceptions import BadPasswordError


class BaseSeller(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=50)


class CreateSeller(BaseSeller):
    password: str
    address: str
    zip_code: int

    @field_validator("password")
    @classmethod
    def password_no_null_bytes(cls, v: str) -> str:
        if "\x00" in v:
            raise BadPasswordError("Password cannot contain null character")
        return v


class ReadSeller(BaseSeller):
    id: UUID
