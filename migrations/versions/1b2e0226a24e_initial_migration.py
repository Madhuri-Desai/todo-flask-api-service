"""Initial migration.

Revision ID: 1b2e0226a24e
Revises: 
Create Date: 2024-06-09 11:27:28.507033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b2e0226a24e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('priority', sa.String(length=50), nullable=True),
    sa.Column('status', sa.String(length=64), nullable=True),
    sa.Column('cancelled', sa.Boolean(), nullable=True),
    sa.Column('reminder', sa.Date(), nullable=True),
    sa.Column('recurring', sa.String(length=64), nullable=True),
    sa.Column('recurring_interval', sa.Integer(), nullable=True),
    sa.Column('next_occurrence', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reminder',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('remind_at', sa.DateTime(), nullable=False),
    sa.Column('notification_method', sa.String(length=50), nullable=False),
    sa.Column('sent', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reminder')
    op.drop_table('tasks')
    # ### end Alembic commands ###
