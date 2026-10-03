"""create user_reports table and add shadow ban columns to users

Revision ID: 0005_create_user_reports_and_shadow_ban
Revises: 0004_create_flatmate_reviews_and_saved_listings
Create Date: 2026-10-02 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0005_create_user_reports_and_shadow_ban'
down_revision: Union[str, None] = '0004_create_flatmate_reviews_and_saved_listings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add shadow ban columns to users table
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_shadow_banned', sa.Boolean(), nullable=False, server_default=sa.text('false')))
        batch_op.add_column(sa.Column('shadow_banned_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.add_column(sa.Column('shadow_ban_reason', sa.String(length=255), nullable=True))

    # Create user_reports table
    op.create_table(
        'user_reports',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('reporter_id', sa.String(length=36), nullable=False),
        sa.Column('reported_user_id', sa.String(length=36), nullable=False),
        sa.Column('reason', sa.String(length=50), nullable=False),
        sa.Column('details', sa.Text(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='PENDING'),
        sa.Column('admin_notes', sa.String(length=500), nullable=True),
        sa.Column('action_taken', sa.String(length=50), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['reported_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reporter_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_reports_id'), 'user_reports', ['id'], unique=False)
    op.create_index(op.f('ix_user_reports_reporter_id'), 'user_reports', ['reporter_id'], unique=False)
    op.create_index(op.f('ix_user_reports_reported_user_id'), 'user_reports', ['reported_user_id'], unique=False)
    op.create_index(op.f('ix_user_reports_reason'), 'user_reports', ['reason'], unique=False)
    op.create_index(op.f('ix_user_reports_status'), 'user_reports', ['status'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_reports_status'), table_name='user_reports')
    op.drop_index(op.f('ix_user_reports_reason'), table_name='user_reports')
    op.drop_index(op.f('ix_user_reports_reported_user_id'), table_name='user_reports')
    op.drop_index(op.f('ix_user_reports_reporter_id'), table_name='user_reports')
    op.drop_index(op.f('ix_user_reports_id'), table_name='user_reports')
    op.drop_table('user_reports')

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('shadow_ban_reason')
        batch_op.drop_column('shadow_banned_at')
        batch_op.drop_column('is_shadow_banned')
