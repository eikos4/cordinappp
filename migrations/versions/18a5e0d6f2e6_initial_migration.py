"""Initial migration

Revision ID: 18a5e0d6f2e6
Revises: 
Create Date: 2025-01-12 03:21:35.173986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18a5e0d6f2e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('meetings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('agenda', sa.Text(), nullable=True),
    sa.Column('minutes', sa.Text(), nullable=True),
    sa.Column('location', sa.String(length=200), nullable=True),
    sa.Column('created_by_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('meeting_participants',
    sa.Column('meeting_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('meeting_id', 'user_id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('priority', sa.String(length=20), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('comments', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('assigned_to', sa.Integer(), nullable=True),
    sa.Column('meeting_id', sa.Integer(), nullable=True),
    sa.Column('dependent_task_id', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('updated_by', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
    sa.ForeignKeyConstraint(['dependent_task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['meeting_id'], ['meetings.id'], ),
    sa.ForeignKeyConstraint(['updated_by'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task_participants',
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('task_id', 'user_id')
    )
    op.create_table('task_progress_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('progress', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task_progress_history')
    op.drop_table('task_participants')
    op.drop_table('tasks')
    op.drop_table('meeting_participants')
    op.drop_table('meetings')
    op.drop_table('users')
    # ### end Alembic commands ###
