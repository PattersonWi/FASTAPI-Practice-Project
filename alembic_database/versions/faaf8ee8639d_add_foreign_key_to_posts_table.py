"""add Foreign Key to Posts table

Revision ID: faaf8ee8639d
Revises: b9c5f840b2ce
Create Date: 2022-08-17 23:41:04.001049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'faaf8ee8639d'
down_revision = 'b9c5f840b2ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key("Posts_FK_Users", source_table="Posts", referent_table="Users", local_cols=["user_id"], remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("Posts_FK_Users", table_name="Posts")
    pass
