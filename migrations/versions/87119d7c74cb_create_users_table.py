
"""create users table

Revision ID: 87119d7c74cb
Revises: 94c565605142
Create Date: 2026-11-19 19:39:26.194867
"""

from alembic import op
import sqlalchemy as sa


revision = '87119d7c74cb'
down_revision = '94c565605142'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('email', sa.String(length=254), nullable=False),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
        sa.UniqueConstraint('username', name=op.f('uq_users_username')),
        sa.UniqueConstraint('email', name=op.f('uq_users_email'))
    )


def downgrade():
    op.drop_table('users')
