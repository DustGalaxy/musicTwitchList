"""update order 2.0

Revision ID: 97d592da891b
Revises: 8a081c7ca2bd
Create Date: 2024-02-20 23:35:21.851292

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97d592da891b'
down_revision: Union[str, None] = '8a081c7ca2bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('video_id', sa.String(), nullable=True))
    op.add_column('order', sa.Column('title', sa.String(), nullable=True))
    op.add_column('order', sa.Column('image_url', sa.String(), nullable=True))
    op.add_column('order', sa.Column('length', sa.Integer(), nullable=True))
    op.drop_column('order', 'url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_column('order', 'length')
    op.drop_column('order', 'image_url')
    op.drop_column('order', 'title')
    op.drop_column('order', 'video_id')
    # ### end Alembic commands ###