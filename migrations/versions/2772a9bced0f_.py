"""empty message

Revision ID: 2772a9bced0f
Revises: 459ebc762542
Create Date: 2022-09-01 10:40:51.462108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2772a9bced0f'
down_revision = '459ebc762542'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('disposisi', sa.Column('nama_bidang', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('disposisi', 'nama_bidang')
    # ### end Alembic commands ###