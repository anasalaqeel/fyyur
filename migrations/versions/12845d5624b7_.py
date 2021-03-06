"""empty message

Revision ID: 12845d5624b7
Revises: d41799eb67a1
Create Date: 2020-05-28 20:13:11.384486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12845d5624b7'
down_revision = 'd41799eb67a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('artist', sa.Column('show_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'artist', 'show', ['show_id'], ['id'])
    op.add_column('venue', sa.Column('show_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'venue', 'show', ['show_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'venue', type_='foreignkey')
    op.drop_column('venue', 'show_id')
    op.drop_constraint(None, 'artist', type_='foreignkey')
    op.drop_column('artist', 'show_id')
    op.drop_table('show')
    # ### end Alembic commands ###
