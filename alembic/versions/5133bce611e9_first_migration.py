"""first migration

Revision ID: 5133bce611e9
Revises: 
Create Date: 2022-03-05 14:25:43.892192

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5133bce611e9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comapnies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nip', sa.String(), nullable=True),
    sa.Column('regon', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comapnies_id'), 'comapnies', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comapnies_id'), table_name='comapnies')
    op.drop_table('comapnies')
    # ### end Alembic commands ###