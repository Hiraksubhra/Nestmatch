"""create listings, amenities, and listing_photos tables

Revision ID: 0002_create_listings_and_amenities_tables
Revises: 0001_create_users_table
Create Date: 2026-09-30 16:10:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0002_create_listings_and_amenities_tables'
down_revision: Union[str, None] = '0001_create_users_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Amenities table
    op.create_table(
        'amenities',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('label', sa.String(length=100), nullable=False),
        sa.Column('icon', sa.String(length=100), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_amenities_name'), 'amenities', ['name'], unique=True)

    # Listings table
    op.create_table(
        'listings',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('landlord_id', sa.String(length=36), nullable=False),
        sa.Column('title', sa.String(length=300), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('property_type', sa.String(length=50), nullable=False, server_default='PG'),
        sa.Column('rent_amount', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('deposit_amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('rent_period', sa.String(length=20), nullable=False, server_default='MONTHLY'),
        sa.Column('address_line1', sa.String(length=300), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('locality', sa.String(length=150), nullable=True),
        sa.Column('state', sa.String(length=100), nullable=True),
        sa.Column('pincode', sa.String(length=10), nullable=True),
        sa.Column('latitude', sa.Numeric(precision=10, scale=7), nullable=True),
        sa.Column('longitude', sa.Numeric(precision=10, scale=7), nullable=True),
        sa.Column('university_proximity', sa.JSON(), nullable=True),
        sa.Column('gender_preference', sa.String(length=20), nullable=False, server_default='ANY'),
        sa.Column('furnished_status', sa.String(length=20), nullable=False, server_default='FURNISHED'),
        sa.Column('available_from', sa.Date(), nullable=True),
        sa.Column('min_stay_months', sa.Integer(), nullable=False, server_default='3'),
        sa.Column('max_occupancy', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='PENDING_VERIFICATION'),
        sa.Column('rejection_reason', sa.Text(), nullable=True),
        sa.Column('is_featured', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('views_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['landlord_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listings_id'), 'listings', ['id'], unique=False)
    op.create_index(op.f('ix_listings_landlord_id'), 'listings', ['landlord_id'], unique=False)
    op.create_index(op.f('ix_listings_city'), 'listings', ['city'], unique=False)
    op.create_index(op.f('ix_listings_status'), 'listings', ['status'], unique=False)

    # Listing Photos table
    op.create_table(
        'listing_photos',
        sa.Column('id', sa.String(length=36), nullable=False),
        sa.Column('listing_id', sa.String(length=36), nullable=False),
        sa.Column('url', sa.String(length=500), nullable=False),
        sa.Column('public_id', sa.String(length=255), nullable=True),
        sa.Column('is_cover', sa.Boolean(), nullable=False, server_default=sa.text('false')),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_listing_photos_id'), 'listing_photos', ['id'], unique=False)
    op.create_index(op.f('ix_listing_photos_listing_id'), 'listing_photos', ['listing_id'], unique=False)

    # Listing Amenities Join table
    op.create_table(
        'listing_amenities',
        sa.Column('listing_id', sa.String(length=36), nullable=False),
        sa.Column('amenity_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['amenity_id'], ['amenities.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('listing_id', 'amenity_id')
    )


def downgrade() -> None:
    op.drop_table('listing_amenities')
    op.drop_index(op.f('ix_listing_photos_listing_id'), table_name='listing_photos')
    op.drop_index(op.f('ix_listing_photos_id'), table_name='listing_photos')
    op.drop_table('listing_photos')
    op.drop_index(op.f('ix_listings_status'), table_name='listings')
    op.drop_index(op.f('ix_listings_city'), table_name='listings')
    op.drop_index(op.f('ix_listings_landlord_id'), table_name='listings')
    op.drop_index(op.f('ix_listings_id'), table_name='listings')
    op.drop_table('listings')
    op.drop_index(op.f('ix_amenities_name'), table_name='amenities')
    op.drop_table('amenities')
