"""add content column in posts table

Revision ID: 9f30e259692c
Revises: e211f2bdb955
Create Date: 2024-11-24 15:15:00.585580

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f30e259692c'
down_revision: Union[str, None] = 'e211f2bdb955'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
