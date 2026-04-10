from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class BaseSeller(BaseModel):
    name: str = Field(max_length=30)
    email: EmailStr = Field(max_length=50)


class CreateSeller(BaseSeller):
    password: str
    address: str
    zip_code: int


class ReadSeller(BaseSeller):
    id: UUID
