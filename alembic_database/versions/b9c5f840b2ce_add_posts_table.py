"""add Posts table

Revision ID: b9c5f840b2ce
Revises: 225acf43b8f6
Create Date: 2022-08-17 23:38:59.394507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9c5f840b2ce'
down_revision = '225acf43b8f6'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table(
    'Posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('height', sa.Float(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('last_modified', sa.TIMESTAMP(timezone=True), server_default = sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    )


    pass


def downgrade() -> None:
    op.drop_table("Posts")
    pass
