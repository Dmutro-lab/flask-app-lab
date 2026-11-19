from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SQLAlchemyEnum, ForeignKey, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import db


class PostCategory(Enum):
    NEWS = "news"
    PUBLICATION = "publication"
    TECH = "tech"
    OTHER = "other"


post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


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
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    user: Mapped["User | None"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
    )

    def __repr__(self):
        return f"<Post {self.id}: {self.title!r}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    posts: Mapped[list[Post]] = relationship(
        secondary=post_tags,
        back_populates="tags",
    )

    def __repr__(self):
        return f"<Tag {self.id}: {self.name!r}>"
