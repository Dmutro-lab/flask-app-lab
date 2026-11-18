
"""Add created_at with server_default

Revision ID: ace40ba8a07c
Revises: 1029f52da3ca
Create Date: 2026-11-18 11:11:41.834449
"""
from alembic import op
import sqlalchemy as sa


revision = 'ace40ba8a07c'
down_revision = '1029f52da3ca'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('products', recreate='always') as batch_op:
        batch_op.add_column(
            sa.Column(
                'created_at',
                sa.DateTime(timezone=True),
                server_default=sa.text('(CURRENT_TIMESTAMP)'),
                nullable=False
            )
        )


def downgrade():
    with op.batch_alter_table('products', recreate='always') as batch_op:
        batch_op.drop_column('created_at')
