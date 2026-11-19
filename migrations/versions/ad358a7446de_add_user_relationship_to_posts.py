
"""add user relationship to posts

Revision ID: ad358a7446de
Revises: 87119d7c74cb
"""

from alembic import op
import sqlalchemy as sa


revision = 'ad358a7446de'
down_revision = '87119d7c74cb'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(
            sa.Column('user_id', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            'fk_posts_user_id_users',
            'users',
            ['user_id'],
            ['id']
        )
        batch_op.drop_column('author')


def downgrade():
    with op.batch_alter_table('posts') as batch_op:
        batch_op.add_column(
            sa.Column(
                'author',
                sa.String(length=20),
                nullable=False,
                server_default='Anonymous'
            )
        )
        batch_op.drop_constraint(
            'fk_posts_user_id_users',
            type_='foreignkey'
        )
        batch_op.drop_column('user_id')
