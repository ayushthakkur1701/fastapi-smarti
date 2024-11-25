"""add foreign key to post table

Revision ID: 9f2c49a5aea9
Revises: 5ab67855e82a
Create Date: 2024-11-24 17:51:37.866433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f2c49a5aea9'
down_revision: Union[str, None] = '5ab67855e82a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_users_fk',source_table="posts",referent_table="users",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column('posts','owner_id')
    pass
