"""add last few columns in posts table 

Revision ID: 346d90f5e164
Revises: 9f2c49a5aea9
Create Date: 2024-11-24 18:03:23.387707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '346d90f5e164'
down_revision: Union[str, None] = '9f2c49a5aea9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),nullable=False
                                    ,server_default='True'),)
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()')),)
    pass


def downgrade() -> None:
    op.drop_column('published',table_name='posts')
    op.drop_column('created_at',table_name='posts')
    pass
