"""Company migration

Revision ID: a12b479361ca
Revises: f00ac8ee9bca
Create Date: 2024-03-13 15:37:48.855544
Created By: Berezanskiy Daniil
"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import mysql

revision = 'a12b479361ca'
down_revision = 'f00ac8ee9bca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('companies',
    sa.Column('id', mysql.BIGINT(unsigned=True), autoincrement=True, nullable=False),
    sa.Column('business_id', sa.String(length=768), nullable=False),
    sa.Column('url', sa.String(length=768), nullable=False),
    sa.Column('name', sa.String(length=1024), nullable=False),
    sa.Column('category', sa.String(length=768), nullable=False),
    sa.Column('address', sa.Text(), nullable=False),
    sa.Column('country', sa.String(length=6), nullable=False),
    sa.Column('state', sa.String(length=2), nullable=False),
    sa.Column('city', sa.String(length=40), nullable=False),
    sa.Column('street', sa.String(length=768), nullable=True),
    sa.Column('postal_code', sa.String(length=10), nullable=False),
    sa.Column('website', sa.String(length=768), nullable=True),
    sa.Column('image_url', sa.String(length=768), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('fax', sa.String(length=20), nullable=True),
    sa.Column('work_hours', sa.JSON(), nullable=True),
    sa.Column('user_score', sa.String(length=5), nullable=True),
    sa.Column('reviews_quantity', sa.BIGINT(), nullable=True),
    sa.Column('accredited_score', sa.String(length=2), nullable=False),
    sa.Column('accredited_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('foundation_date', sa.TIMESTAMP(), nullable=True),
    sa.Column('years_old', sa.BIGINT(), nullable=True),
    sa.Column('instagram', sa.String(length=768), nullable=True),
    sa.Column('facebook', sa.String(length=768), nullable=True),
    sa.Column('twitter', sa.String(length=768), nullable=True),
    sa.Column('management', sa.JSON(), nullable=True),
    sa.Column('contact', sa.JSON(), nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('sent_to_customer', mysql.TIMESTAMP(), server_default=None, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('business_id')
    )
    op.create_index(op.f('ix_companies_updated_at'), 'companies', ['updated_at'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_companies_updated_at'), table_name='companies')
    op.drop_table('companies')
