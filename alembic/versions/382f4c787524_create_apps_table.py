"""create apps table

Revision ID: 382f4c787524
Revises: a6b991c79189
Create Date: 2024-12-09 06:37:33.986897

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '382f4c787524'
down_revision: Union[str, None] = 'a6b991c79189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_name', sa.String(), nullable=False),
    sa.Column('play_store_version', sa.String(), nullable=True),
    sa.Column('app_store_version', sa.String(), nullable=True),
    sa.Column('microsoft_store_version', sa.String(), nullable=True),
    sa.Column('force_update', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.Column('is_pause', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('package_name')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###