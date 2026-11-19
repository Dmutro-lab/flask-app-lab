
"""add tags and post_tags tables

Revision ID: bc5f2e1064c6
Revises: ad358a7446de
Create Date: 2026-11-19 19:54:59.732115
"""
from alembic import op
import sqlalchemy as sa


revision = 'bc5f2e1064c6'
down_revision = 'ad358a7446de'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_tags')),
        sa.UniqueConstraint('name', name=op.f('uq_tags_name'))
    )

    op.create_table(
        'post_tags',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['post_id'], ['posts.id'],
            name=op.f('fk_post_tags_post_id_posts')
        ),
        sa.ForeignKeyConstraint(
            ['tag_id'], ['tags.id'],
            name=op.f('fk_post_tags_tag_id_tags')
        ),
        sa.PrimaryKeyConstraint('post_id', 'tag_id', name=op.f('pk_post_tags'))
    )


def downgrade():
    op.drop_table('post_tags')
    op.drop_table('tags')
