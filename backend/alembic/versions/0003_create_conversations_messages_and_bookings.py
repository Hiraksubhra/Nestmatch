"""create conversations, messages, and booking_requests tables

Revision ID: 0003_create_conversations_messages_and_bookings
Revises: 0002_create_listings_and_amenities_tables
Create Date: 2026-09-30 22:45:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0003_create_conversations_messages_and_bookings'
down_revision: Union[str, None] = '0002_create_listings_and_amenities_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Conversations table
    op.create_table(
        'conversations',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('listing_id', sa.String(length=36), nullable=True),
        sa.Column('student_id', sa.String(length=36), nullable=False),
        sa.Column('landlord_id', sa.String(length=36), nullable=False),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='OPEN'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['landlord_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('listing_id', 'student_id', name='uq_conversation_listing_student')
    )
    op.create_index(op.f('ix_conversations_id'), 'conversations', ['id'], unique=False)
    op.create_index(op.f('ix_conversations_listing_id'), 'conversations', ['listing_id'], unique=False)
    op.create_index(op.f('ix_conversations_student_id'), 'conversations', ['student_id'], unique=False)
    op.create_index(op.f('ix_conversations_landlord_id'), 'conversations', ['landlord_id'], unique=False)

    # Messages table
    op.create_table(
        'messages',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('conversation_id', sa.String(length=36), nullable=False),
        sa.Column('sender_id', sa.String(length=36), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('message_type', sa.String(length=20), nullable=False, server_default='TEXT'),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_messages_id'), 'messages', ['id'], unique=False)
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)
    op.create_index(op.f('ix_messages_sender_id'), 'messages', ['sender_id'], unique=False)

    # Booking Requests table
    op.create_table(
        'booking_requests',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('listing_id', sa.String(length=36), nullable=False),
        sa.Column('student_id', sa.String(length=36), nullable=False),
        sa.Column('landlord_id', sa.String(length=36), nullable=False),
        sa.Column('move_in_date', sa.Date(), nullable=False),
        sa.Column('duration_months', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING'),
        sa.Column('message', sa.Text(), nullable=True),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['student_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['landlord_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_booking_requests_id'), 'booking_requests', ['id'], unique=False)
    op.create_index(op.f('ix_booking_requests_listing_id'), 'booking_requests', ['listing_id'], unique=False)
    op.create_index(op.f('ix_booking_requests_student_id'), 'booking_requests', ['student_id'], unique=False)
    op.create_index(op.f('ix_booking_requests_landlord_id'), 'booking_requests', ['landlord_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_booking_requests_landlord_id'), table_name='booking_requests')
    op.drop_index(op.f('ix_booking_requests_student_id'), table_name='booking_requests')
    op.drop_index(op.f('ix_booking_requests_listing_id'), table_name='booking_requests')
    op.drop_index(op.f('ix_booking_requests_id'), table_name='booking_requests')
    op.drop_table('booking_requests')

    op.drop_index(op.f('ix_messages_sender_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_index(op.f('ix_messages_id'), table_name='messages')
    op.drop_table('messages')

    op.drop_index(op.f('ix_conversations_landlord_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_student_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_listing_id'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_id'), table_name='conversations')
    op.drop_table('conversations')
