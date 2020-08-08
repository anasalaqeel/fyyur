"""empty message

Revision ID: 616f9f7fa3ad
Revises: 12845d5624b7
Create Date: 2020-05-28 20:14:24.463003

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '616f9f7fa3ad'
down_revision = '12845d5624b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('artist', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('venue', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('artist', 'show_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
