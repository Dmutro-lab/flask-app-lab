"""Initial posts table.

Revision ID: 001_initial_posts
Revises:
Create Date: 2026-11-08
"""
from alembic import op
import sqlalchemy as sa

revision = "001_initial_posts"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=150), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("posted", sa.DateTime(), nullable=False),
        sa.Column("category", sa.Enum("news", "publication", "tech", "other", name="postcategory", native_enum=False), nullable=False),
    )


def downgrade():
    op.drop_table("posts")
