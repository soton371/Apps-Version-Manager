"""first migration

Revision ID: 3a206d5442f7
Revises: 
Create Date: 2025-01-31 20:58:05.985650

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a206d5442f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('app_name', sa.String(), nullable=True),
    sa.Column('package_name', sa.String(), nullable=False),
    sa.Column('play_store_version', sa.String(), nullable=True),
    sa.Column('app_store_version', sa.String(), nullable=True),
    sa.Column('microsoft_store_version', sa.String(), nullable=True),
    sa.Column('force_update', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.Column('is_pause', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.Column('app_icon', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('play_store_link', sa.String(), nullable=True),
    sa.Column('app_store_link', sa.String(), nullable=True),
    sa.Column('microsoft_store_link', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('package_name')
    )
    op.create_table('audit_trail',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sector', sa.String(), nullable=True),
    sa.Column('task_by', sa.String(), nullable=True),
    sa.Column('task', sa.String(), nullable=True),
    sa.Column('impact', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('exception_report',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('package_name', sa.String(), nullable=True),
    sa.Column('url', sa.String(), nullable=True),
    sa.Column('payload', sa.String(), nullable=True),
    sa.Column('exception', sa.String(), nullable=True),
    sa.Column('exception_line', sa.String(), nullable=True),
    sa.Column('fixed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.String(), nullable=True),
    sa.Column('updated_by', sa.String(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('exception_report')
    op.drop_table('audit_trail')
    op.drop_table('apps')
    # ### end Alembic commands ###
