"""empty message

Revision ID: d935dfe4c277
Revises: ce4f05cdd455
Create Date: 2020-05-29 13:42:19.353443

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd935dfe4c277'
down_revision = 'ce4f05cdd455'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('website', sa.String(length=500), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('artist', 'website')
    # ### end Alembic commands ###
