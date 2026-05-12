from typing import Literal

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int]  = mapped_column(primary_key=True, autoincrement=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    gender: Mapped[Literal["Мужчина", "Женщина"]]
    phone: Mapped[str]
    email: Mapped[str]
    address: Mapped[str]