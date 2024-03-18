"""initial  migration

Revision ID: f00ac8ee9bca
Revises:
Create Date: 2024-03-07 01:04:47.562207
Created By: Berezanskiy Daniil
"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import mysql

revision = 'f00ac8ee9bca'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('urls',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('url', sa.String(length=768), nullable=False),
    sa.Column('status', mysql.MEDIUMINT(unsigned=True), server_default=sa.text('0'), nullable=False),
    sa.Column('exception', mysql.TEXT(), nullable=True),
    sa.UniqueConstraint('url'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_urls_status'), 'urls', ['status'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_urls_status'), table_name='urls')
    op.drop_table('urls')
