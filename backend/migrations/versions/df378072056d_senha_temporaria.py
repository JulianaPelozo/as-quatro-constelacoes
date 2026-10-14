"""senha temporaria

Revision ID: df378072056d
Revises: e3662c207992
Create Date: 2026-10-14 14:01:46.655242

"""
from alembic import op
import sqlalchemy as sa


revision = 'df378072056d'
down_revision = 'e3662c207992'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('precisa_trocar_senha', sa.Boolean(), server_default=sa.false(), nullable=False))


def downgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('precisa_trocar_senha')

