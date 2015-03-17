"""empty message

Revision ID: 2e8077fe0870
Revises: 2d01630380b2
Create Date: 2015-03-17 03:08:17.161474

"""

# revision identifiers, used by Alembic.
revision = '2e8077fe0870'
down_revision = '2d01630380b2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transition', sa.Column('ps_notification_code', sa.String(length=39), nullable=True))
    op.add_column('transition', sa.Column('ps_payload', sa.Text(), nullable=True))
    op.add_column('transition', sa.Column('type', sa.String(length=20), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('transition', 'type')
    op.drop_column('transition', 'ps_payload')
    op.drop_column('transition', 'ps_notification_code')
    ### end Alembic commands ###
