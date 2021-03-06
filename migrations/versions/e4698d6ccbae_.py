"""empty message

Revision ID: e4698d6ccbae
Revises: f8eab1a03dae
Create Date: 2020-05-28 21:56:04.684312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4698d6ccbae'
down_revision = 'f8eab1a03dae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'address')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('address', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
