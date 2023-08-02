"""create posts table'



Revision ID: e5eb1e542f46
Revises: 
Create Date: 2023-07-24 09:08:22.611517

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5eb1e542f46'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
