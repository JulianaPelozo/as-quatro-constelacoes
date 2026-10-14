"""historias e capitulos

Revision ID: 5f433c26b151
Revises: df378072056d
Create Date: 2026-10-14 14:19:20.807686

"""
from alembic import op
import sqlalchemy as sa


revision = '5f433c26b151'
down_revision = 'df378072056d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('historias',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=200), nullable=False),
    sa.Column('autora_id', sa.Integer(), nullable=False),
    sa.Column('link', sa.String(length=500), nullable=False),
    sa.Column('no_circulo', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('criada_em', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['autora_id'], ['usuarios.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('historias', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_historias_autora_id'), ['autora_id'], unique=False)

    op.create_table('capitulos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('historia_id', sa.Integer(), nullable=False),
    sa.Column('numero', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(length=200), nullable=True),
    sa.Column('link', sa.String(length=500), nullable=False),
    sa.Column('criado_em', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['historia_id'], ['historias.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('historia_id', 'numero', name='uq_capitulos_historia_numero')
    )
    with op.batch_alter_table('capitulos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_capitulos_historia_id'), ['historia_id'], unique=False)


    if op.get_bind().dialect.name == 'postgresql':
        op.execute('ALTER TABLE historias ENABLE ROW LEVEL SECURITY')
        op.execute('ALTER TABLE capitulos ENABLE ROW LEVEL SECURITY')


def downgrade():
    with op.batch_alter_table('capitulos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_capitulos_historia_id'))

    op.drop_table('capitulos')
    with op.batch_alter_table('historias', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_historias_autora_id'))

    op.drop_table('historias')
