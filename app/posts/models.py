from datetime import datetime
from enum import Enum

from sqlalchemy import Enum as SQLAlchemyEnum, String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    category: Mapped[PostCategory] = mapped_column(
        SQLAlchemyEnum(PostCategory, values_callable=lambda enum: [item.value for item in enum], native_enum=False),
        nullable=False,
        default=PostCategory.OTHER,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="1")
    author: Mapped[str] = mapped_column(String(20), nullable=False, default="Anonymous", server_default="Anonymous")

    def __repr__(self):
        return f"<Post {self.id}: {self.title!r}>"
