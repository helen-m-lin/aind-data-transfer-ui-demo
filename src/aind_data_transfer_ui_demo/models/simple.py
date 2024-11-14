"""Simple models for testing pydantic forms ui generation"""
import enum
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    SecretStr,
    field_validator,
)

# FastUI #######################
class LoginForm(BaseModel):
    email: EmailStr = Field(title='Email Address', description="Try 'x@y' to trigger server side validation")
    password: SecretStr


class ToolEnum(str, enum.Enum):
    hammer = 'hammer'
    screwdriver = 'screwdriver'
    saw = 'saw'
    claw_hammer = 'claw_hammer'


class SelectForm(BaseModel):
    select_single: ToolEnum = Field(title='Select Single')
    select_multiple: list[ToolEnum] = Field(title='Select Multiple')
    # NOTE: uses /search endpoint to populate options dynamically
    search_select_single: str = Field(json_schema_extra={'search_url': '/api/forms/search'})
    search_select_multiple: list[str] = Field(json_schema_extra={'search_url': '/api/forms/search'})

    @field_validator('select_multiple', 'search_select_multiple', mode='before')
    @classmethod
    def correct_select_multiple(cls, v: list[str]) -> list[str]:
        if isinstance(v, list):
            return v
        else:
            return [v]