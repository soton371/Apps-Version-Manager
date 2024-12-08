"""add microsoft column

Revision ID: 865d111dd857
Revises: e922b13aba2c
Create Date: 2024-12-08 20:19:57.701720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '865d111dd857'
down_revision: Union[str, None] = 'e922b13aba2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
