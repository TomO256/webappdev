"""empty message

Revision ID: 088bf2649b51
Revises: 5921db068c3b
Create Date: 2024-12-02 20:16:26.816790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '088bf2649b51'
down_revision = '5921db068c3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blanks', sa.Integer(), nullable=True))
        batch_op.drop_column('blank')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blank', sa.INTEGER(), nullable=True))
        batch_op.drop_column('blanks')

    # ### end Alembic commands ###
