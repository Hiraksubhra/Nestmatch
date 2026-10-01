"""create flatmate_profiles, reviews, and saved_listings tables

Revision ID: 0004_create_flatmate_reviews_and_saved_listings
Revises: 0003_create_conversations_messages_and_bookings
Create Date: 2026-10-01 15:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0004_create_flatmate_reviews_and_saved_listings'
down_revision: Union[str, None] = '0003_create_conversations_messages_and_bookings'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Flatmate Profiles table
    op.create_table(
        'flatmate_profiles',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('budget_min', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('budget_max', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('preferred_city', sa.String(length=100), nullable=True),
        sa.Column('preferred_university', sa.String(length=200), nullable=True),
        sa.Column('preferred_locality', sa.String(length=150), nullable=True),
        sa.Column('move_in_date', sa.Date(), nullable=True),
        sa.Column('move_in_flexibility', sa.Integer(), nullable=False, server_default='7'),
        sa.Column('gender', sa.String(length=20), nullable=True),
        sa.Column('bio', sa.String(length=280), nullable=True),
        sa.Column('lifestyle_tags', sa.JSON(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', name='uq_flatmate_user_id')
    )
    op.create_index(op.f('ix_flatmate_profiles_id'), 'flatmate_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_flatmate_profiles_user_id'), 'flatmate_profiles', ['user_id'], unique=True)
    op.create_index(op.f('ix_flatmate_profiles_preferred_city'), 'flatmate_profiles', ['preferred_city'], unique=False)
    op.create_index(op.f('ix_flatmate_profiles_is_active'), 'flatmate_profiles', ['is_active'], unique=False)

    # Reviews table
    op.create_table(
        'reviews',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('listing_id', sa.String(length=36), nullable=False),
        sa.Column('reviewer_id', sa.String(length=36), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=True),
        sa.Column('body', sa.Text(), nullable=True),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['reviewer_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('listing_id', 'reviewer_id', name='uq_listing_reviewer'),
        sa.CheckConstraint('rating >= 1 AND rating <= 5', name='ck_review_rating_range')
    )
    op.create_index(op.f('ix_reviews_id'), 'reviews', ['id'], unique=False)
    op.create_index(op.f('ix_reviews_listing_id'), 'reviews', ['listing_id'], unique=False)
    op.create_index(op.f('ix_reviews_reviewer_id'), 'reviews', ['reviewer_id'], unique=False)

    # Saved Listings table
    op.create_table(
        'saved_listings',
        sa.Column('user_id', sa.String(length=36), nullable=False),
        sa.Column('listing_id', sa.String(length=36), nullable=False),
        sa.Column('saved_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'listing_id')
    )
    op.create_index(op.f('ix_saved_listings_user_id'), 'saved_listings', ['user_id'], unique=False)
    op.create_index(op.f('ix_saved_listings_listing_id'), 'saved_listings', ['listing_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_saved_listings_listing_id'), table_name='saved_listings')
    op.drop_index(op.f('ix_saved_listings_user_id'), table_name='saved_listings')
    op.drop_table('saved_listings')

    op.drop_index(op.f('ix_reviews_reviewer_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_listing_id'), table_name='reviews')
    op.drop_index(op.f('ix_reviews_id'), table_name='reviews')
    op.drop_table('reviews')

    op.drop_index(op.f('ix_flatmate_profiles_is_active'), table_name='flatmate_profiles')
    op.drop_index(op.f('ix_flatmate_profiles_preferred_city'), table_name='flatmate_profiles')
    op.drop_index(op.f('ix_flatmate_profiles_user_id'), table_name='flatmate_profiles')
    op.drop_index(op.f('ix_flatmate_profiles_id'), table_name='flatmate_profiles')
    op.drop_table('flatmate_profiles')
