from typing import Literal

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class UserSchemaResponse(BaseModel):
    first_name: str = Field(..., max_length=64, description="Имя")
    last_name: str = Field(..., max_length=64, description="Фамилия")
    gender: Literal["Мужчина", "Женщина"] = Field(..., description="Пол")
    phone: str = Field(..., max_length=18, description="Телефон")
    email: EmailStr = Field(..., description="Электронная почта")
    address: str = Field(..., max_length=512, description="Место проживания")
    
    links: dict[str, HttpUrl] = Field(..., description="Ссылки")

class LoadNewUsers(BaseModel):
    count: int = Field(ge=1, default=1, description="Количество пользователей для загрузки")