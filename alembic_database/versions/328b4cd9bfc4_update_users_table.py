"""update users table

Revision ID: 328b4cd9bfc4
Revises: fd7d2003af4a
Create Date: 2022-08-23 20:26:50.984906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '328b4cd9bfc4'
down_revision = 'fd7d2003af4a'
branch_labels = None
depends_on = None

def upgrade() -> None:

    
    op.drop_column("Users", "email")

    pass


def downgrade() -> None:
    pass

