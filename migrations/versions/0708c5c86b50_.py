"""empty message

Revision ID: 0708c5c86b50
Revises: eefc3faf9edf
Create Date: 2022-11-14 16:50:33.979832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0708c5c86b50'
down_revision = 'eefc3faf9edf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_activity', 'kegiatan',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.Text(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('daily_activity', 'kegiatan',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
    # ### end Alembic commands ###