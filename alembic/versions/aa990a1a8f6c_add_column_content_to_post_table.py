"""add column content to post table

Revision ID: aa990a1a8f6c
Revises: 026a098f1869
Create Date: 2023-10-26 02:54:22.415042

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa990a1a8f6c'
down_revision: Union[str, None] = '026a098f1869'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("content", sa.String()))
    # pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    # pass
