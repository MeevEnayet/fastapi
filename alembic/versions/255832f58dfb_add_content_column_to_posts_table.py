"""add content column to posts table

Revision ID: 255832f58dfb
Revises: e5eb1e542f46
Create Date: 2023-07-24 09:40:16.034156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '255832f58dfb'
down_revision = 'e5eb1e542f46'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
