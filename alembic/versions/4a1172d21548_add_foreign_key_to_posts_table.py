"""add foreign key to posts table

Revision ID: 4a1172d21548
Revises: 7dca12481bf6
Create Date: 2023-08-01 07:12:05.605071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1172d21548'
down_revision = '7dca12481bf6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk', source_table="posts", referent_table="users",local_cols=['owner_id'], remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts','owner_id')
    pass
