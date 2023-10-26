"""add foreignkey to posts

Revision ID: 52fb2e9781b8
Revises: 13df17fc9c4e
Create Date: 2023-10-26 03:22:20.488596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52fb2e9781b8'
down_revision: Union[str, None] = '13df17fc9c4e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.add_column("posts", sa.Column("owner_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")))
    # or
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
  

def downgrade() -> None:
    # op.drop_column("posts", "owner_id") 
    # or
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')