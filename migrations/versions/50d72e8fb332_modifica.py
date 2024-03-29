"""MODIFICA

Revision ID: 50d72e8fb332
Revises: d58f54e263c1
Create Date: 2022-03-10 16:25:07.605797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50d72e8fb332'
down_revision = 'd58f54e263c1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbextrato', schema=None) as batch_op:
        batch_op.add_column(sa.Column('data_modificado', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tbextrato', schema=None) as batch_op:
        batch_op.drop_column('data_modificado')

    # ### end Alembic commands ###
