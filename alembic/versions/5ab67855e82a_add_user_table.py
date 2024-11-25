"""add user table

Revision ID: 5ab67855e82a
Revises: 9f30e259692c
Create Date: 2024-11-24 16:45:25.591212

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ab67855e82a'
down_revision: Union[str, None] = '9f30e259692c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('email',sa.String(),nullable=False,unique=True),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
