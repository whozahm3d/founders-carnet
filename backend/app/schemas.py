from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


UserRole = Literal["founder", "talent", "mentor", "investor"]


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)
    consent_accepted: bool


class LinkedInSignInRequest(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    authorization_code: str = Field(min_length=1, max_length=512)
    consent_accepted: bool


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(hide_input_in_errors=True)

    email: EmailStr
    password: str


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ConsentStatusRead(BaseModel):
    consent_type: str
    consent_version: str
    withdrawn: bool
    withdrawn_at: datetime | None


class DeletionRequestRead(BaseModel):
    requested_at: datetime
    deletion_scheduled_for: datetime
    account_disabled: bool


class FounderProfileWrite(BaseModel):
    bio: str | None = Field(default=None, max_length=2000)
    location: str | None = Field(default=None, max_length=255)
    consent_accepted: bool


class FounderProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bio: str | None
    location: str | None
    consent_version: str
    consented_at: datetime


class StartupCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=5000)
    sector: str = Field(min_length=1, max_length=100)
    stage: Literal["idea", "mvp", "growth", "scaling"]
    location: str = Field(min_length=1, max_length=255)
    business_model: str = Field(min_length=1, max_length=255)
    traction_summary: str = Field(min_length=1, max_length=5000)
    customer_count: int = Field(default=0, ge=0)
    monthly_revenue: Decimal | None = Field(default=None, ge=0)
    skills: list[str] = Field(default_factory=list, max_length=50)
    funding_need_min: Decimal | None = Field(default=None, ge=0)
    funding_need_max: Decimal | None = Field(default=None, ge=0)


class StartupUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=5000)
    sector: str | None = Field(default=None, min_length=1, max_length=100)
    stage: Literal["idea", "mvp", "growth", "scaling"] | None = None
    location: str | None = Field(default=None, min_length=1, max_length=255)
    business_model: str | None = Field(default=None, min_length=1, max_length=255)
    traction_summary: str | None = Field(default=None, min_length=1, max_length=5000)
    customer_count: int | None = Field(default=None, ge=0)
    monthly_revenue: Decimal | None = Field(default=None, ge=0)
    skills: list[str] | None = Field(default=None, max_length=50)
    funding_need_min: Decimal | None = Field(default=None, ge=0)
    funding_need_max: Decimal | None = Field(default=None, ge=0)


class StartupRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    sector: str
    stage: str
    location: str
    business_model: str
    traction_summary: str
    customer_count: int
    monthly_revenue: Decimal | None
    skills: list[str]
    funding_need_min: Decimal | None
    funding_need_max: Decimal | None
    is_verified: bool
