"""Add active

Revision ID: 1029f52da3ca
Revises: 90fc89591713
Create Date: 2026-11-18 11:03:25.407674
"""
from alembic import op
import sqlalchemy as sa


revision = '1029f52da3ca'
down_revision = '90fc89591713'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column(
        'products',
        sa.Column(
            'active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )


def downgrade():
    op.drop_column('products', 'active')