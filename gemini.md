# Gemini.md — Student Housing Platform: Master Project Reference

> **Purpose:** This file is the single source of truth for the entire project. Every team member and AI assistant working on this codebase should read this file before making any decisions. It covers product vision, functional requirements, architecture, data models, API contracts, sprint planning, and team assignments.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Competitive Analysis & Inspiration](#2-competitive-analysis--inspiration)
3. [Product Requirements (PRD)](#3-product-requirements-prd)
4. [Functional Requirements](#4-functional-requirements)
5. [User Personas](#5-user-personas)
6. [User Flows & Wireframe Descriptions](#6-user-flows--wireframe-descriptions)
7. [Technical Architecture](#7-technical-architecture)
8. [Data Models](#8-data-models)
9. [API Contract](#9-api-contract)
10. [Tech Stack Decision Log](#10-tech-stack-decision-log)
11. [Project Structure](#11-project-structure)
12. [Environment Variables & Configuration](#12-environment-variables--configuration)
13. [Sprint Plan](#13-sprint-plan)
14. [Team Assignments](#14-team-assignments)
15. [Definition of Done](#15-definition-of-done)
16. [Git & Branching Strategy](#16-git--branching-strategy)

---

## 1. Project Overview

**Product Name:** NestMatch  
**Tagline:** *Find your space, find your people.*  
**Type:** Web Application (Mobile PWA-ready; native mobile deferred)

### Vision

NestMatch is a student-first housing platform that solves three core problems:

1. **Discovery** — Finding verified, campus-proximate housing with transparent pricing.
2. **Safety** — Eliminating scams by keeping all payments and communication inside the platform.
3. **Social Fit** — Matching roommates by lifestyle, not just location.

### Target Market

- University/college students in India seeking off-campus accommodation.
- Property owners (individual landlords, PG operators, co-living startups) listing to student audiences.

---

## 2. Competitive Analysis & Inspiration

| Platform | Key Takeaway to Adopt |
|---|---|
| **AmberStudent / Student.com** | Verified listings, virtual tours, digestible lease-term icons/tags, clean search UX |
| **HousingAnywhere** | In-platform payments (no direct bank transfers), end-to-end digital booking flow, scam prevention |
| **SpareRoom** | "Flatmate Profile" — users list themselves as room-seekers, enabling social roommate matching |
| **Stanza Living / ZoloStays** | Campus-proximity filters, bundled amenities (food, laundry, Wi-Fi) in a single rental package, community events |

**Our Differentiation:** Combine all four pillars — verified listings + safe payments + roommate matching + bundled amenity discovery — in a single platform built specifically for the Indian student housing market.

---

## 3. Product Requirements (PRD)

### 3.1 Goals

- P0 (Must Have): Listing discovery, listing detail page, user auth, landlord posting, in-app inquiry/messaging.
- P1 (Should Have): Roommate matching (flatmate profiles), safe payment integration, booking flow.
- P2 (Nice to Have): Virtual tour embed, review & rating system, saved searches with email alerts.

### 3.2 Non-Goals (v1)

- Native mobile apps (iOS/Android).
- Direct payment gateway integration (stub with "Request to Book" CTA).
- AI-based recommendation engine.

### 3.3 Success Metrics

- User can search and find a relevant listing in < 3 clicks.
- Listing detail page loads in < 2 seconds.
- Landlord can publish a verified listing in < 10 minutes.
- Zero direct payment CTAs that bypass the platform (all money flows through platform).

---

## 4. Functional Requirements

### 4.1 Authentication & Authorization

- FR-AUTH-01: Users can register with email + password.
- FR-AUTH-02: Users can log in via email/password and Google OAuth.
- FR-AUTH-03: JWT-based session management with refresh tokens.
- FR-AUTH-04: Roles: `STUDENT`, `LANDLORD`, `ADMIN`.
- FR-AUTH-05: Email verification on signup.
- FR-AUTH-06: Password reset via email link.

### 4.2 Listing Management (Landlord)

- FR-LIST-01: Landlord can create a listing with: title, description, address, rent, deposit, available-from date, property type (PG / Apartment / Shared Room / Studio), gender preference, amenities, photos (up to 10), and house rules.
- FR-LIST-02: Listings have a status: `DRAFT`, `PENDING_VERIFICATION`, `ACTIVE`, `INACTIVE`, `ARCHIVED`.
- FR-LIST-03: Admin can approve or reject listings (moves them from `PENDING` → `ACTIVE` or `REJECTED`).
- FR-LIST-04: Landlord can edit and deactivate their listings.
- FR-LIST-05: Amenity tags: Wi-Fi, AC, Laundry, Meals Included, Parking, Gym, Power Backup, Security.

### 4.3 Listing Discovery (Student)

- FR-DISC-01: Search by city, locality, or university name.
- FR-DISC-02: Filter by: rent range, property type, gender preference, amenities, furnished status, distance to university.
- FR-DISC-03: Sort by: rent (low-high / high-low), date listed (newest), distance.
- FR-DISC-04: Map view of results using embedded map (Leaflet.js with OpenStreetMap).
- FR-DISC-05: Listing card shows: photo, title, price/month, key amenities as icons, verified badge, distance to campus.
- FR-DISC-06: Pagination (20 results per page) and infinite scroll option.

### 4.4 Listing Detail Page

- FR-DETAIL-01: Full photo gallery with lightbox.
- FR-DETAIL-02: Amenity grid with icons.
- FR-DETAIL-03: Lease terms summarized as tags (e.g., "6-month min", "No Pets", "Bills Included").
- FR-DETAIL-04: Landlord profile card with response rate.
- FR-DETAIL-05: "Request to Visit" / "Enquire Now" CTA that opens in-app chat thread.
- FR-DETAIL-06: Map showing listing location (exact address blurred until inquiry confirmed).
- FR-DETAIL-07: Similar listings carousel.
- FR-DETAIL-08: Save listing (bookmark) for logged-in users.

### 4.5 Roommate Matching (Flatmate Profiles)

- FR-ROOM-01: Students can create a "Looking For Room" profile with: budget, preferred locality/university, move-in date, lifestyle tags (Early Riser, Night Owl, Vegetarian, Non-Smoker, etc.), gender, short bio.
- FR-ROOM-02: Listings can show "Seeking Flatmates" section with compatible profiles.
- FR-ROOM-03: Students can browse other flatmate profiles and send a "Connect" request.
- FR-ROOM-04: Flatmate matching score based on overlapping lifestyle tags.

### 4.6 Messaging & Inquiries

- FR-MSG-01: Students can send an inquiry from a listing detail page, creating a conversation thread.
- FR-MSG-02: Landlord sees all inquiries in a unified inbox.
- FR-MSG-03: Real-time messaging via WebSockets (or polling fallback).
- FR-MSG-04: Message history is persisted.
- FR-MSG-05: System messages for booking milestones ("Landlord accepted visit request").

### 4.7 Booking Flow (Stub in v1)

- FR-BOOK-01: Student clicks "Request to Book" → submits move-in date & duration.
- FR-BOOK-02: Landlord receives notification and can Accept/Decline.
- FR-BOOK-03: On acceptance, both parties see a "Booking Confirmed" state with contact details revealed.
- FR-BOOK-04: Actual payment is out of scope for v1 (stub CTA: "Pay via Platform — Coming Soon").

### 4.8 Reviews & Ratings

- FR-REV-01: After a completed booking, students can leave a rating (1–5 stars) and text review.
- FR-REV-02: Reviews are displayed on the listing detail page.
- FR-REV-03: Average rating is shown on listing cards.

### 4.9 Admin Panel

- FR-ADMIN-01: Dashboard with key metrics (total listings, pending verifications, active users).
- FR-ADMIN-02: Listing verification queue — approve/reject with a reason.
- FR-ADMIN-03: User management (ban, role change).
- FR-ADMIN-04: Reported listings review.

---

## 5. User Personas

### Persona A — Aanya, The First-Year Student
- 18 years old, just got admission to a Tier-1 college in Pune.
- Searching from her hometown (remote browsing), worried about scams.
- Needs: verified listings, virtual tours, parent-shareable links, safe inquiry without sharing personal number.

### Persona B — Rakesh, The Working Landlord
- 45 years old, owns a 3BHK near a campus, wants to rent out two rooms.
- Not tech-savvy; needs a simple listing flow with clear status updates.
- Needs: easy listing creation, WhatsApp-like chat, notifications when a student inquires.

### Persona C — Priya, The Social Matcher
- 21 years old, 3rd year, knows the city but wants to find compatible flatmates.
- Needs: flatmate profile, lifestyle matching, ability to join existing shared apartments.

---

## 6. User Flows & Wireframe Descriptions

### Flow 1: Student Searches and Inquires About a Listing

```
[Home Page]
   |
   ├── Search Bar (City / University / Locality) + "Search" button
   |
   v
[Search Results Page]
   |
   ├── Left Sidebar: Filters (Rent, Type, Amenities, Gender, Distance)
   ├── Main Area: Listing Cards Grid (2-col desktop, 1-col mobile)
   ├── Top Right: Sort Dropdown | Map Toggle
   |
   ├── Click a Listing Card
   v
[Listing Detail Page]
   |
   ├── Photo Gallery (hero image + thumbnails)
   ├── Title + Price + Verified Badge
   ├── Amenity Icons Row
   ├── Lease Term Tags
   ├── Description
   ├── Map (blurred pin)
   ├── Landlord Card (avatar, name, response rate)
   ├── [Enquire Now] CTA   [Save Listing] CTA
   |
   ├── Click "Enquire Now" → Redirect to login if not authenticated
   v
[Chat/Inquiry Thread]
   |
   ├── Pre-filled message: "Hi, I'm interested in [Listing Name]..."
   ├── Message input
   └── Send → Landlord notified
```

### Flow 2: Landlord Posts a Listing

```
[Landlord Dashboard]
   |
   ├── "Post New Listing" button
   v
[Listing Creation Wizard — 4 Steps]
   |
   ├── Step 1: Basic Info (Title, Type, Address, Rent, Deposit)
   ├── Step 2: Amenities & Rules (checkbox grid, free-text house rules)
   ├── Step 3: Photos (drag-drop upload, reorder, cover photo select)
   ├── Step 4: Review & Submit
   |
   v
[Status: PENDING_VERIFICATION]
   |
   ├── Admin reviews listing
   └── Email notification → "Your listing is now LIVE"
```

### Flow 3: Roommate Matching

```
[Student Profile Page]
   |
   ├── "Create Flatmate Profile" button
   v
[Flatmate Profile Form]
   |
   ├── Budget, University, Move-in Date
   ├── Lifestyle Tags (multi-select chips)
   ├── Short bio (140 chars)
   └── [Publish Profile]
   |
   v
[Browse Flatmates Page]
   |
   ├── Filter by University, Budget, Lifestyle Tags
   ├── Profile Cards: Avatar, Name (first only), Tags, Compatibility %
   └── [Connect] button → Opens message thread
```

### Wireframe Layout Descriptions

#### Home Page Layout
```
┌─────────────────────────────────────────────────────┐
│  NAVBAR: Logo | Search | [Login] [Sign Up]          │
├─────────────────────────────────────────────────────┤
│                                                     │
│  HERO: Full-width illustrated campus scene          │
│  H1: "Find Your Perfect Student Home"               │
│  SearchBar: [City or University...] [Search]        │
│  Popular: Pune · Mumbai · Bangalore · Delhi         │
│                                                     │
├─────────────────────────────────────────────────────┤
│  HOW IT WORKS: 3-column icon steps                  │
│  [Search] → [Inquire] → [Book Safely]               │
├─────────────────────────────────────────────────────┤
│  FEATURED LISTINGS: Horizontal scroll card row      │
├─────────────────────────────────────────────────────┤
│  ROOMMATE MATCHING CTA: Full-width tinted band      │
│  "Looking for flatmates? Create your profile →"     │
├─────────────────────────────────────────────────────┤
│  FOOTER: Links | Social | © NestMatch 2025          │
└─────────────────────────────────────────────────────┘
```

#### Search Results Page Layout
```
┌────────────┬──────────────────────────────────────┐
│ FILTERS    │  SORT BAR              [Map View]     │
│            ├──────────────────────────────────────┤
│ Rent Range │  [Card] [Card]                        │
│ Type       │  [Card] [Card]                        │
│ Amenities  │  [Card] [Card]                        │
│ Gender     │                                       │
│ Distance   │  Pagination: < 1 2 3 ... >           │
└────────────┴──────────────────────────────────────┘
```

---

## 7. Technical Architecture

### 7.1 Architecture Pattern

**Three-Tier Architecture with Layered Backend**

```
┌─────────────────────────────────────────────────────────┐
│                     CLIENT TIER                          │
│          React 18 + Vite  (SPA, hosted on Vercel)       │
└────────────────────┬────────────────────────────────────┘
                     │ HTTPS / REST / WebSocket
┌────────────────────▼────────────────────────────────────┐
│                    API TIER                              │
│          FastAPI (Python 3.12)                          │
│   ┌──────────────┐  ┌────────────┐  ┌────────────────┐  │
│   │  Auth Router │  │  Listings  │  │  Messaging     │  │
│   │  /api/auth   │  │  /api/list │  │  /api/messages │  │
│   └──────────────┘  └────────────┘  └────────────────┘  │
│   ┌──────────────┐  ┌────────────┐  ┌────────────────┐  │
│   │  Users       │  │  Bookings  │  │  Admin         │  │
│   │  /api/users  │  │  /api/book │  │  /api/admin    │  │
│   └──────────────┘  └────────────┘  └────────────────┘  │
│          │                  │                            │
│   ┌──────▼──────┐    ┌──────▼──────┐                    │
│   │  SQLAlchemy │    │   Celery    │ (background tasks)  │
│   │    ORM      │    │  + Redis    │                     │
│   └──────┬──────┘    └─────────────┘                    │
└──────────┼──────────────────────────────────────────────┘
           │
┌──────────▼──────────────────────────────────────────────┐
│                    DATA TIER                             │
│   PostgreSQL 16          Redis (Cache + Queue)          │
│   (Primary DB)           Cloudinary (Image Storage)     │
└─────────────────────────────────────────────────────────┘
```

### 7.2 Tech Stack Decision

#### Frontend: React 18 + Vite
- **Why Vite:** Sub-second HMR, native ESM, fast builds. Superior DX over CRA.
- **State:** Zustand (global: auth, filters) + React Query / TanStack Query (server state, caching).
- **Routing:** React Router v6.
- **UI:** Tailwind CSS + shadcn/ui components.
- **Maps:** Leaflet.js + React-Leaflet (OpenStreetMap — free, no API key needed).
- **Forms:** React Hook Form + Zod validation.
- **Real-time:** WebSocket via native API / socket.io-client.

#### Backend: FastAPI (Python 3.12)

**Decision: FastAPI over Spring Boot**

| Factor | FastAPI | Spring Boot |
|---|---|---|
| Team onboarding (5-person student team) | ✅ Python — widely known | ❌ Java — steeper learning curve |
| Speed of development (5 sprints) | ✅ Rapid, minimal boilerplate | ❌ Verbose config |
| Async support | ✅ Native async/await | ⚠️ Reactive (more complex) |
| Auto-generated API docs | ✅ Swagger UI built-in | ⚠️ Requires springdoc |
| ML/AI integration later | ✅ Python ecosystem | ❌ Harder |
| Production-ready | ✅ Used by Netflix, Microsoft | ✅ Enterprise-grade |

**Verdict: FastAPI** wins for a 5-person student team on a time-boxed project.

- **ORM:** SQLAlchemy 2.0 (async) + Alembic (migrations).
- **Auth:** python-jose (JWT) + passlib (bcrypt hashing) + OAuth via Authlib.
- **Validation:** Pydantic v2.
- **Background Tasks:** Celery + Redis (email notifications, image processing).
- **File Uploads:** Cloudinary SDK.
- **Email:** SendGrid (free tier: 100 emails/day).
- **WebSockets:** FastAPI native WebSocket support.

#### Database: PostgreSQL 16

**Decision: PostgreSQL over MySQL / MongoDB**

- Strong JSON support (for flexible amenity metadata).
- Full-text search with `pg_trgm` (listing search without Elasticsearch in v1).
- PostGIS extension for geo-proximity queries.
- Heroku Postgres / Neon.tech free tiers available.

**Caching & Queues:** Redis (Upstash free tier or local Docker).

#### Infrastructure
- **Frontend Hosting:** Vercel (free for students).
- **Backend Hosting:** Railway.app or Render.com (free tier, auto-deploys from GitHub).
- **Database:** Neon.tech (serverless Postgres, free tier, 0.5 GB).
- **Image Storage:** Cloudinary (free tier: 25 GB).
- **CI/CD:** GitHub Actions.

---

## 8. Data Models

### 8.1 Entity Relationship Overview

```
Users ──< Listings (landlord creates)
Users ──< FlatmateProfiles (student creates, 1:1)
Listings ──< Photos
Listings ──< Amenities (M:M via ListingAmenity)
Listings ──< Reviews
Users ──< Conversations
Conversations ──< Messages
Users ──< SavedListings (M:M)
Listings ──< BookingRequests
```

### 8.2 Table Definitions

#### `users`
```sql
CREATE TABLE users (
    id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email         VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255),                    -- NULL for OAuth users
    full_name     VARCHAR(255) NOT NULL,
    avatar_url    VARCHAR(500),
    role          VARCHAR(20) NOT NULL DEFAULT 'STUDENT',  -- STUDENT | LANDLORD | ADMIN
    phone         VARCHAR(20),
    is_verified   BOOLEAN DEFAULT FALSE,
    is_active     BOOLEAN DEFAULT TRUE,
    oauth_provider VARCHAR(50),                    -- 'google' | NULL
    oauth_id       VARCHAR(255),
    created_at    TIMESTAMPTZ DEFAULT NOW(),
    updated_at    TIMESTAMPTZ DEFAULT NOW()
);
```

#### `listings`
```sql
CREATE TABLE listings (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    landlord_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(300) NOT NULL,
    description     TEXT,
    property_type   VARCHAR(50) NOT NULL,  -- PG | APARTMENT | SHARED_ROOM | STUDIO
    rent_amount     NUMERIC(10, 2) NOT NULL,
    deposit_amount  NUMERIC(10, 2),
    rent_period     VARCHAR(20) DEFAULT 'MONTHLY',
    address_line1   VARCHAR(300),
    city            VARCHAR(100) NOT NULL,
    locality        VARCHAR(150),
    state           VARCHAR(100),
    pincode         VARCHAR(10),
    latitude        NUMERIC(10, 7),
    longitude       NUMERIC(10, 7),
    university_proximity JSONB,            -- [{"name": "Pune University", "distance_km": 1.2}]
    gender_preference VARCHAR(20) DEFAULT 'ANY', -- MALE | FEMALE | ANY
    furnished_status  VARCHAR(20) DEFAULT 'FURNISHED', -- FURNISHED | SEMI | UNFURNISHED
    available_from  DATE,
    min_stay_months INTEGER DEFAULT 3,
    max_occupancy   INTEGER DEFAULT 1,
    status          VARCHAR(30) DEFAULT 'DRAFT',  -- DRAFT | PENDING_VERIFICATION | ACTIVE | INACTIVE | ARCHIVED | REJECTED
    rejection_reason TEXT,
    is_featured     BOOLEAN DEFAULT FALSE,
    views_count     INTEGER DEFAULT 0,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_listings_city ON listings(city);
CREATE INDEX idx_listings_status ON listings(status);
CREATE INDEX idx_listings_landlord ON listings(landlord_id);
CREATE INDEX idx_listings_geo ON listings USING GIST (point(longitude, latitude));
```

#### `listing_photos`
```sql
CREATE TABLE listing_photos (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id   UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    url          VARCHAR(500) NOT NULL,
    public_id    VARCHAR(255),                -- Cloudinary public_id for deletion
    is_cover     BOOLEAN DEFAULT FALSE,
    sort_order   INTEGER DEFAULT 0,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);
```

#### `amenities`
```sql
CREATE TABLE amenities (
    id       SERIAL PRIMARY KEY,
    name     VARCHAR(100) UNIQUE NOT NULL,  -- 'wifi', 'ac', 'laundry', etc.
    label    VARCHAR(100) NOT NULL,          -- Display label
    icon     VARCHAR(100)                    -- Icon identifier
);

CREATE TABLE listing_amenities (
    listing_id  UUID REFERENCES listings(id) ON DELETE CASCADE,
    amenity_id  INTEGER REFERENCES amenities(id),
    PRIMARY KEY (listing_id, amenity_id)
);
```

#### `flatmate_profiles`
```sql
CREATE TABLE flatmate_profiles (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id         UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    budget_min      NUMERIC(10, 2),
    budget_max      NUMERIC(10, 2) NOT NULL,
    preferred_city  VARCHAR(100),
    preferred_university VARCHAR(200),
    preferred_locality VARCHAR(150),
    move_in_date    DATE,
    move_in_flexibility INTEGER DEFAULT 7,  -- days
    gender          VARCHAR(20),
    bio             VARCHAR(280),
    lifestyle_tags  TEXT[],                  -- ['early_riser', 'vegetarian', 'non_smoker']
    is_active       BOOLEAN DEFAULT TRUE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `conversations`
```sql
CREATE TABLE conversations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id  UUID REFERENCES listings(id) ON DELETE SET NULL,
    student_id  UUID NOT NULL REFERENCES users(id),
    landlord_id UUID NOT NULL REFERENCES users(id),
    status      VARCHAR(30) DEFAULT 'OPEN',   -- OPEN | CLOSED | BOOKED
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    updated_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (listing_id, student_id)
);
```

#### `messages`
```sql
CREATE TABLE messages (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_id       UUID NOT NULL REFERENCES users(id),
    content         TEXT NOT NULL,
    message_type    VARCHAR(20) DEFAULT 'TEXT',  -- TEXT | SYSTEM | MEDIA
    is_read         BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
```

#### `booking_requests`
```sql
CREATE TABLE booking_requests (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id      UUID NOT NULL REFERENCES listings(id),
    student_id      UUID NOT NULL REFERENCES users(id),
    landlord_id     UUID NOT NULL REFERENCES users(id),
    move_in_date    DATE NOT NULL,
    duration_months INTEGER NOT NULL,
    status          VARCHAR(30) DEFAULT 'PENDING',  -- PENDING | ACCEPTED | DECLINED | CANCELLED
    message         TEXT,
    responded_at    TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
```

#### `reviews`
```sql
CREATE TABLE reviews (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    listing_id  UUID NOT NULL REFERENCES listings(id) ON DELETE CASCADE,
    reviewer_id UUID NOT NULL REFERENCES users(id),
    rating      SMALLINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title       VARCHAR(200),
    body        TEXT,
    is_verified BOOLEAN DEFAULT FALSE,   -- based on completed booking
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (listing_id, reviewer_id)
);
```

#### `saved_listings`
```sql
CREATE TABLE saved_listings (
    user_id     UUID REFERENCES users(id) ON DELETE CASCADE,
    listing_id  UUID REFERENCES listings(id) ON DELETE CASCADE,
    saved_at    TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (user_id, listing_id)
);
```

---

## 9. API Contract

> Base URL: `https://api.nestmatch.in/api/v1`  
> All endpoints return JSON. Auth endpoints use Bearer token in `Authorization` header.

### 9.1 Auth Endpoints

```
POST   /auth/register          Register new user
POST   /auth/login             Email/password login → {access_token, refresh_token}
POST   /auth/refresh           Refresh access token
POST   /auth/logout            Invalidate refresh token
POST   /auth/google            Google OAuth callback
POST   /auth/forgot-password   Send reset email
POST   /auth/reset-password    Reset with token
GET    /auth/verify-email      Verify email with token
```

### 9.2 User Endpoints

```
GET    /users/me               Get current user profile
PUT    /users/me               Update profile
GET    /users/{id}             Get public user profile
```

### 9.3 Listing Endpoints

```
GET    /listings               Search/list listings (query params: city, type, min_rent, max_rent, amenities, gender, sort, page, limit)
POST   /listings               Create listing (LANDLORD only)
GET    /listings/{id}          Get listing detail
PUT    /listings/{id}          Update listing (owner only)
DELETE /listings/{id}          Archive listing (owner only)
POST   /listings/{id}/photos   Upload photos (multipart/form-data)
DELETE /listings/{id}/photos/{photo_id}  Delete a photo
GET    /listings/my            Get landlord's own listings
POST   /listings/{id}/save     Save/unsave listing toggle
GET    /listings/saved         Get saved listings
```

### 9.4 Flatmate Profile Endpoints

```
GET    /flatmates              Browse flatmate profiles (filter: city, university, budget, tags)
POST   /flatmates              Create/update my flatmate profile
GET    /flatmates/me           Get my flatmate profile
GET    /flatmates/{id}         Get a specific flatmate profile
DELETE /flatmates/me           Deactivate my profile
```

### 9.5 Messaging Endpoints

```
GET    /conversations          List my conversations
POST   /conversations          Start new conversation (includes listing_id)
GET    /conversations/{id}     Get conversation + messages
POST   /conversations/{id}/messages   Send a message
PUT    /conversations/{id}/messages/{msg_id}/read  Mark as read
WS     /ws/conversations/{id}  WebSocket for real-time messages
```

### 9.6 Booking Endpoints

```
POST   /bookings               Create booking request
GET    /bookings               List my booking requests (student or landlord)
GET    /bookings/{id}          Get booking detail
PUT    /bookings/{id}/accept   Landlord accepts
PUT    /bookings/{id}/decline  Landlord declines
PUT    /bookings/{id}/cancel   Student cancels
```

### 9.7 Review Endpoints

```
GET    /listings/{id}/reviews  Get reviews for a listing
POST   /listings/{id}/reviews  Submit review (student, after booking)
```

### 9.8 Admin Endpoints

```
GET    /admin/listings/pending   Listings awaiting verification
PUT    /admin/listings/{id}/approve
PUT    /admin/listings/{id}/reject  (body: {reason})
GET    /admin/users
PUT    /admin/users/{id}/ban
GET    /admin/stats              Dashboard metrics
```

### 9.9 Standard Response Format

```json
// Success
{
  "success": true,
  "data": { ... },
  "message": "optional message"
}

// Paginated
{
  "success": true,
  "data": [...],
  "meta": {
    "total": 240,
    "page": 1,
    "limit": 20,
    "pages": 12
  }
}

// Error
{
  "success": false,
  "error": {
    "code": "LISTING_NOT_FOUND",
    "message": "The requested listing does not exist.",
    "details": {}
  }
}
```

---

## 10. Tech Stack Decision Log

| Decision | Choice | Reason | Alternatives Considered |
|---|---|---|---|
| Frontend Framework | React 18 + Vite | Specified in brief, industry standard | — |
| Backend Framework | FastAPI | Python familiarity, speed, auto-docs | Spring Boot (rejected: Java overhead) |
| Primary Database | PostgreSQL 16 | Geo queries, full-text search, JSON | MySQL (no PostGIS), MongoDB (no relations) |
| ORM | SQLAlchemy 2.0 | Async support, Alembic migrations | Tortoise ORM, Django ORM |
| Cache / Queue | Redis | Celery integration, session store | RabbitMQ (heavier) |
| Image Storage | Cloudinary | Free tier, transformation API | AWS S3 (costs money), local (not scalable) |
| State Management | Zustand + TanStack Query | Lightweight, composable | Redux Toolkit (verbose) |
| CSS | Tailwind CSS | Utility-first, fast iteration | Styled Components (runtime cost) |
| UI Components | shadcn/ui | Accessible, Tailwind-native, copy-paste | MUI (opinionated), Ant Design (heavy) |
| Maps | Leaflet + React-Leaflet | Free, OpenStreetMap, no API key | Google Maps (paid) |
| Auth | JWT + Google OAuth | Stateless, scalable | Sessions + cookies |
| Email | SendGrid | Free tier, reliable | Mailgun, SMTP |
| Hosting (FE) | Vercel | Free for students, auto-deploy | Netlify |
| Hosting (BE) | Railway.app | Docker support, free tier | Render, Fly.io |

---

## 11. Project Structure

### Frontend (`/frontend`)

```
frontend/
├── public/
├── src/
│   ├── assets/              # Static images, fonts
│   ├── components/
│   │   ├── ui/              # shadcn/ui base components (Button, Card, Input...)
│   │   ├── layout/          # Navbar, Footer, Sidebar, Layout wrapper
│   │   ├── listings/        # ListingCard, ListingGrid, ListingFilters, PhotoGallery
│   │   ├── flatmates/       # FlatmateCard, FlatmateFilters, ProfileForm
│   │   ├── messaging/       # ChatWindow, MessageBubble, ConversationList
│   │   └── shared/          # AmenityIcon, StarRating, BadgeVerified, MapView
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Search.jsx
│   │   ├── ListingDetail.jsx
│   │   ├── FlatmatesBrowse.jsx
│   │   ├── auth/            # Login.jsx, Register.jsx, ForgotPassword.jsx
│   │   ├── dashboard/       # LandlordDashboard.jsx, StudentDashboard.jsx
│   │   ├── landlord/        # CreateListing.jsx, EditListing.jsx, MyListings.jsx
│   │   ├── messaging/       # Inbox.jsx, ConversationThread.jsx
│   │   └── admin/           # AdminDashboard.jsx, PendingListings.jsx
│   ├── hooks/               # useAuth, useListings, useSearch, useMessaging
│   ├── store/               # Zustand stores: authStore.js, filterStore.js
│   ├── services/            # api.js (axios instance), listings.js, auth.js...
│   ├── lib/                 # cn utility, validators, formatters
│   ├── constants/           # amenities.js, propertyTypes.js, routes.js
│   ├── router/              # routes.jsx (React Router config, protected routes)
│   ├── types/               # JSDoc types or PropTypes
│   ├── App.jsx
│   └── main.jsx
├── .env.example
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── package.json
```

### Backend (`/backend`)

```
backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── listings.py
│   │   │   ├── flatmates.py
│   │   │   ├── conversations.py
│   │   │   ├── bookings.py
│   │   │   ├── reviews.py
│   │   │   └── admin.py
│   │   └── router.py        # Aggregates all routers
│   ├── core/
│   │   ├── config.py        # Settings (pydantic BaseSettings)
│   │   ├── security.py      # JWT, password hashing
│   │   ├── dependencies.py  # get_current_user, get_db
│   │   └── exceptions.py    # Custom exception handlers
│   ├── db/
│   │   ├── base.py          # SQLAlchemy Base
│   │   ├── session.py       # Async engine + session factory
│   │   └── init_db.py       # Seed amenities, admin user
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── listing.py
│   │   ├── message.py
│   │   ├── booking.py
│   │   └── review.py
│   ├── schemas/             # Pydantic request/response schemas
│   │   ├── user.py
│   │   ├── listing.py
│   │   ├── message.py
│   │   └── booking.py
│   ├── services/            # Business logic layer
│   │   ├── auth_service.py
│   │   ├── listing_service.py
│   │   ├── messaging_service.py
│   │   ├── cloudinary_service.py
│   │   └── email_service.py
│   ├── tasks/               # Celery tasks
│   │   └── notifications.py
│   └── main.py              # FastAPI app factory
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── test_auth.py
│   ├── test_listings.py
│   └── conftest.py
├── .env.example
├── alembic.ini
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 12. Environment Variables & Configuration

### Frontend `.env`

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_WS_BASE_URL=ws://localhost:8000
VITE_GOOGLE_CLIENT_ID=<google_oauth_client_id>
VITE_CLOUDINARY_CLOUD_NAME=<your_cloud_name>
```

### Backend `.env`

```env
# App
APP_ENV=development
SECRET_KEY=<generate: openssl rand -hex 32>
ALLOWED_ORIGINS=http://localhost:5173,https://nestmatch.vercel.app

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/nestmatch_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Google OAuth
GOOGLE_CLIENT_ID=<google_oauth_client_id>
GOOGLE_CLIENT_SECRET=<google_oauth_client_secret>

# Cloudinary
CLOUDINARY_CLOUD_NAME=<cloud_name>
CLOUDINARY_API_KEY=<api_key>
CLOUDINARY_API_SECRET=<api_secret>

# SendGrid
SENDGRID_API_KEY=<sendgrid_api_key>
FROM_EMAIL=noreply@nestmatch.in

# Frontend URL (for email links)
FRONTEND_URL=http://localhost:5173
```

> **NEVER commit `.env` files to Git. Always use `.env.example` templates.**

---

## 13. Sprint Plan

**Total Duration:** 5 Sprints × 2 Weeks = 10 Weeks  
**Team:** 5 Members (see Section 14 for assignments)  
**Ceremony Cadence:** Monday sync (30 min) + Friday demo (1 hr)

### Sprint 0 — Setup & Foundations (Week 1–2)

**Goal:** Every team member has a running local environment. Core scaffolding is in place.

| Task | Owner | Notes |
|---|---|---|
| Initialize GitHub repo, branch strategy, PR templates | Lead (TM1) | See Section 16 |
| Set up Vite + React project, install Tailwind, shadcn/ui | TM2 (Frontend) | |
| Set up FastAPI project structure, Docker Compose | TM3 (Backend Core) | Postgres + Redis containers |
| Configure Alembic + initial migration (users table) | TM3 | |
| Register Cloudinary, SendGrid, Google OAuth accounts | All leads | Save keys in `.env.example` |
| Create Figma file with design tokens + component sketches | TM2 | Reference brandRules.md |
| Set up CI/CD (GitHub Actions: lint + test on PR) | TM1 | |
| Implement User model + Auth endpoints (register, login, JWT) | TM3 | |
| Implement React Router setup + protected routes | TM2 | |
| Deploy skeleton to Vercel (FE) + Railway (BE) | TM1 | |

### Sprint 1 — Listings Core (Week 3–4)

**Goal:** Landlords can post listings. Students can search and view them.

| Task | Owner |
|---|---|
| Listing model, migrations, CRUD endpoints | TM3 |
| Photo upload endpoint + Cloudinary integration | TM3 |
| Amenities seed data + listing_amenities join | TM3 |
| Admin listing approval endpoints | TM3 |
| Search endpoint with filters, pagination, full-text | TM4 (Backend Search/Realtime) |
| Landlord: CreateListing wizard (4-step form) | TM2 |
| Landlord: MyListings page, edit, deactivate | TM2 |
| Search Results page (listing grid + filter sidebar) | TM5 (Frontend Discovery) |
| Listing Detail page (gallery, amenity icons, map) | TM5 |
| Listing Card component | TM5 |
| Home page hero + search bar | TM2 |

### Sprint 2 — Messaging & Booking (Week 5–6)

**Goal:** Students can inquire, landlords can respond. Booking request flow is functional.

| Task | Owner |
|---|---|
| Conversation + Message models + REST endpoints | TM4 |
| WebSocket endpoint for real-time messaging | TM4 |
| Booking Request model + endpoints (create, accept, decline) | TM4 |
| Chat UI (Inbox list + conversation thread) | TM2 |
| "Enquire Now" flow — creates conversation, redirects to chat | TM5 |
| Booking Request UI on listing detail page | TM5 |
| Landlord inquiry notifications (email via Celery) | TM3 |
| Student booking status page | TM5 |

### Sprint 3 — Roommate Matching & Reviews (Week 7–8)

**Goal:** Flatmate profiles are live. Students can browse and connect. Reviews work.

| Task | Owner |
|---|---|
| FlatmateProfile model + CRUD endpoints | TM4 |
| Flatmate search + compatibility score algorithm | TM4 |
| Review model + endpoints | TM3 |
| Flatmate profile creation form | TM2 |
| Browse Flatmates page with filter and cards | TM5 |
| "Connect" button → opens message thread | TM5 |
| Review form on booking completion | TM5 |
| Reviews section on listing detail page | TM5 |
| SavedListings endpoint + UI (bookmark on cards) | TM3 + TM5 |

### Sprint 4 — Admin, Polish & Testing (Week 9–10)

**Goal:** Admin panel live. All flows tested. Performance tuned. Deployment finalized.

| Task | Owner |
|---|---|
| Admin dashboard (metrics endpoint + UI) | TM1 |
| Admin: pending listings queue, approve/reject UI | TM1 |
| Admin: user management table | TM1 |
| End-to-end tests (Playwright or Cypress) | TM1 |
| Backend unit tests (pytest) | TM3 |
| Performance: React Query caching, lazy loading | TM2 |
| Responsive design audit (mobile breakpoints) | TM2 |
| Map view on search results (Leaflet) | TM5 |
| SEO meta tags (React Helmet) | TM2 |
| Error boundaries + 404/500 pages | TM2 |
| Production deployment validation + environment vars | TM1 |

---

## 14. Team Assignments

> Each member owns one vertical slice of the application. They are the decision-maker and reviewer for their area.

| Member | Role Title | Primary Area | Backup Area |
|---|---|---|---|
| **TM1** | Tech Lead & DevOps | CI/CD, deployment, admin panel, E2E tests, code review | Auth |
| **TM2** | Frontend Lead | Auth UI, landlord flows, chat UI, responsive design, design system | Shared components |
| **TM3** | Backend Core | Auth, listing CRUD, photos, admin APIs, email/notifications | Database schema |
| **TM4** | Backend Search & Realtime | Search/filter engine, WebSockets, messaging APIs, booking APIs, flatmate matching | Caching |
| **TM5** | Frontend Discovery | Search page, listing detail, flatmate browse, booking UI, map integration | Reviews UI |

**PR Rule:** Every PR requires review from at least one other member. Own-area PRs can be self-merged after CI passes (for speed), but cross-area PRs need the area owner's approval.

---

## 15. Definition of Done

A feature is "done" when:

- [ ] Functionality works end-to-end in the browser (not just Postman).
- [ ] All new API endpoints have Swagger docs (FastAPI auto-generates; add docstrings).
- [ ] No TypeScript/ESLint errors (frontend) / no flake8 errors (backend).
- [ ] Works on mobile viewport (≥ 375px).
- [ ] PR has been reviewed by at least one teammate.
- [ ] New env variables added to `.env.example`.
- [ ] Migrations run cleanly with `alembic upgrade head`.

---

## 16. Git & Branching Strategy

**Main Branches:**
- `main` — production-ready code only. Protected. Requires PR + passing CI.
- `develop` — integration branch. All feature PRs merge here.

**Feature Branches:**
- Format: `feature/<initials>/<short-description>` — e.g., `feature/tm2/listing-wizard`
- Bugfixes: `fix/<initials>/<short-description>`
- Chores: `chore/setup-ci`

**Commit Message Format (Conventional Commits):**
```
feat(listings): add photo upload with Cloudinary
fix(auth): refresh token expiry not clearing correctly
chore(ci): add pytest to GitHub Actions workflow
```

**PR Template:**
```markdown
## What this PR does
[Short description]

## Related Sprint Task
Sprint X — [Task name]

## Testing done
- [ ] Manual test in browser
- [ ] Unit tests added/passed
- [ ] Mobile viewport checked

## Screenshots (if UI)
```

---

*Last updated: Sprint 0 Setup*  
*Maintained by: TM1 (Tech Lead)*
