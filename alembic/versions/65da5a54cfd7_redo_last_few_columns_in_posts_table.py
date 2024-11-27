"""redo last few columns in posts table 

Revision ID: 65da5a54cfd7
Revises: 346d90f5e164
Create Date: 2024-11-24 18:10:15.213755

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65da5a54cfd7'
down_revision: Union[str, None] = '346d90f5e164'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if 'published' column exists
    # Use a direct query to check for the column existence
    
    pass


def downgrade() -> None:
    
    pass
