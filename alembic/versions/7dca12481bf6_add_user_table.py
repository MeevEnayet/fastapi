"""add User table

Revision ID: 7dca12481bf6
Revises: 255832f58dfb
Create Date: 2023-07-24 09:45:21.693975

"""
from alembic import op
import sqlalchemy as sa
import time


# revision identifiers, used by Alembic.
revision = '7dca12481bf6'
down_revision = '255832f58dfb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
