"""add constraint to users table unique email

Revision ID: 3417be7d7430
Revises: cd62441f93fc
Create Date: 2022-09-09 16:02:44.220791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3417be7d7430'
down_revision = 'cd62441f93fc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_unique_constraint("email", "Users", ["email"])
    


def downgrade() -> None:
    op.drop_constraint("email", "Users", ["email"])  
