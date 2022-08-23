"""add Users table

Revision ID: 225acf43b8f6
Revises: 
Create Date: 2022-08-17 23:37:47.972048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '225acf43b8f6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:


    op.create_table(
    'Users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.Integer(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('last_modified', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint("email")
    )

    pass


def downgrade() -> None:
    op.drop_table("Users")
    pass

