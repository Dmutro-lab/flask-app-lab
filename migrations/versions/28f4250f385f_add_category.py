"""Add category

Revision ID: 28f4250f385f
Revises: 8b5dc7aabc02
Create Date: 2026-11-18 10:56:33.428512
"""
from alembic import op
import sqlalchemy as sa


revision = '28f4250f385f'
down_revision = '8b5dc7aabc02'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=128), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('category_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            'category_id',
            'categories',
            ['category_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint('category_id', type_='foreignkey')
        batch_op.drop_column('category_id')

    op.drop_table('categories')