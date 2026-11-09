"""Add is_active and author fields.

Revision ID: 002_add_active_author
Revises: 001_initial_posts
Create Date: 2026-11-08
"""
from alembic import op
import sqlalchemy as sa

revision = "002_add_active_author"
down_revision = "001_initial_posts"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("posts") as batch_op:
        batch_op.add_column(sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()))
        batch_op.add_column(sa.Column("author", sa.String(length=20), nullable=False, server_default="Anonymous"))


def downgrade():
    with op.batch_alter_table("posts") as batch_op:
        batch_op.drop_column("author")
        batch_op.drop_column("is_active")
