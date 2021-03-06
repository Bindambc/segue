"""created recordings table

Revision ID: 3fd61abd510d
Revises: 561cf7c99269
Create Date: 2015-07-09 17:55:57.813542

"""

# revision identifiers, used by Alembic.
revision = '3fd61abd510d'
down_revision = '561cf7c99269'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recording',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slot_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['slot_id'], ['slot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recording')
    ### end Alembic commands ###
