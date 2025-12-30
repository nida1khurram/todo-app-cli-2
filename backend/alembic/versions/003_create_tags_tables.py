"""Create tags and task_tags tables

Revision ID: 003
Revises: 002
Create Date: 2024-01-03 00:00:00

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_tags_user_id', 'tags', ['user_id'], unique=False)
    op.create_index('ix_tags_name', 'tags', ['name'], unique=False)
    op.create_unique_constraint('unique_user_tag', 'tags', ['user_id', 'name'])

    # Create task_tags junction table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'tag_id'),
    )
    op.create_index('ix_task_tags_task_id', 'task_tags', ['task_id'], unique=False)
    op.create_index('ix_task_tags_tag_id', 'task_tags', ['tag_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_task_tags_tag_id', table_name='task_tags')
    op.drop_index('ix_task_tags_task_id', table_name='task_tags')
    op.drop_table('task_tags')
    op.drop_constraint('unique_user_tag', 'tags', type_='unique')
    op.drop_index('ix_tags_name', table_name='tags')
    op.drop_index('ix_tags_user_id', table_name='tags')
    op.drop_table('tags')
