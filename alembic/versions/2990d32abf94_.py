"""empty message

Revision ID: 2990d32abf94
Revises: 
Create Date: 2022-06-30 11:12:30.922495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2990d32abf94'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('books',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('author', sa.String(100), nullable=False))


def downgrade() -> None:
    op.drop_table('books')
