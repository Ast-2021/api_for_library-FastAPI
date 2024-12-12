"""Initial migration

Revision ID: 01d226ce1799
Revises: 
Create Date: 2024-12-12 04:13:55.968979

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01d226ce1799'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Authors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.CheckConstraint('char_length(last_name) >= 2', name='last_name_min_length'),
    sa.CheckConstraint('char_length(name) >= 2', name='name_min_length'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Authors_id'), 'Authors', ['id'], unique=False)
    op.create_index(op.f('ix_Authors_last_name'), 'Authors', ['last_name'], unique=False)
    op.create_index(op.f('ix_Authors_name'), 'Authors', ['name'], unique=False)
    op.create_table('Books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('available_quantity', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['Authors.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_index(op.f('ix_Books_id'), 'Books', ['id'], unique=False)
    op.create_table('Borrow',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('reader_name', sa.String(), nullable=False),
    sa.Column('date_of_issue', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['Books.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Borrow_id'), 'Borrow', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Borrow_id'), table_name='Borrow')
    op.drop_table('Borrow')
    op.drop_index(op.f('ix_Books_id'), table_name='Books')
    op.drop_table('Books')
    op.drop_index(op.f('ix_Authors_name'), table_name='Authors')
    op.drop_index(op.f('ix_Authors_last_name'), table_name='Authors')
    op.drop_index(op.f('ix_Authors_id'), table_name='Authors')
    op.drop_table('Authors')
    # ### end Alembic commands ###
