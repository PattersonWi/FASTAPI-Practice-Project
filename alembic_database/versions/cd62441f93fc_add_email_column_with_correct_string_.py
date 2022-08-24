"""add email column with correct string type

Revision ID: cd62441f93fc
Revises: 328b4cd9bfc4
Create Date: 2022-08-23 20:35:22.471460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd62441f93fc'
down_revision = '328b4cd9bfc4'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("Users", sa.Column('email', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("Users", "email")
    pass
