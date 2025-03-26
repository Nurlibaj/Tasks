"""Create flowers table

Revision ID: flowers_migration
Revises: users_migration
Create Date: 2023-05-15 12:01:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'flowers_migration'
down_revision = 'users_migration'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('flowers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('count', sa.Integer(), nullable=False),
        sa.Column('price', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_flowers_id'), 'flowers', ['id'], unique=False)
    op.create_index(op.f('ix_flowers_name'), 'flowers', ['name'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_flowers_name'), table_name='flowers')
    op.drop_index(op.f('ix_flowers_id'), table_name='flowers')
    op.drop_table('flowers') 