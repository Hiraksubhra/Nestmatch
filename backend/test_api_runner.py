import os
import sys
import httpx
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
ASSETS_DIR = r"D:\Code\Student_Rental_App\frontend\assets"

def run_tests():
    print("=" * 60)
    print("NESTMATCH API TESTING SUITE WITH REAL ASSETS")
    print("=" * 60)

    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        # Step 1: Health Check
        health = client.get("http://127.0.0.1:8000/health")
        print(f"[1] Server Health: {health.status_code} - {health.json()}")
        assert health.status_code == 200

        # Step 2: Register/Login Landlord
        landlord_email = "landlord.tester@nestmatch.in"
        landlord_pass = "Password123!"
        landlord_res = client.post("/auth/register", json={
            "email": landlord_email,
            "password": landlord_pass,
            "full_name": "Suresh Landlord",
            "role": "LANDLORD"
        })
        if landlord_res.status_code == 409:
            # Login instead
            landlord_res = client.post("/auth/login", json={
                "email": landlord_email,
                "password": landlord_pass
            })
        print(f"[2] Landlord Auth: {landlord_res.status_code}")
        assert landlord_res.status_code in [200, 201]
        landlord_token = landlord_res.json()["data"]["access_token"]
        landlord_headers = {"Authorization": f"Bearer {landlord_token}"}

        # Step 3: Register/Login Student
        student_email = "student.tester@nestmatch.in"
        student_pass = "Password123!"
        student_res = client.post("/auth/register", json={
            "email": student_email,
            "password": student_pass,
            "full_name": "Rohan Student",
            "role": "STUDENT"
        })
        if student_res.status_code == 409:
            student_res = client.post("/auth/login", json={
                "email": student_email,
                "password": student_pass
            })
        print(f"[3] Student Auth: {student_res.status_code}")
        assert student_res.status_code in [200, 201]
        student_token = student_res.json()["data"]["access_token"]
        student_headers = {"Authorization": f"Bearer {student_token}"}

        # Step 4: Register/Login Admin
        admin_email = "admin.tester@nestmatch.in"
        admin_pass = "Password123!"
        admin_res = client.post("/auth/register", json={
            "email": admin_email,
            "password": admin_pass,
            "full_name": "Admin Supervisor",
            "role": "ADMIN"
        })
        if admin_res.status_code == 409:
            admin_res = client.post("/auth/login", json={
                "email": admin_email,
                "password": admin_pass
            })
        print(f"[4] Admin Auth: {admin_res.status_code}")
        assert admin_res.status_code in [200, 201]
        admin_token = admin_res.json()["data"]["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        # Step 5: Landlord creates listing
        listing_payload = {
            "title": "Premium Student PG near Symbiosis Campus",
            "description": "Fully furnished luxury PG with high-speed WiFi, daily meals, AC, and regular housekeeping.",
            "property_type": "PG",
            "rent_amount": 14500.0,
            "deposit_amount": 25000.0,
            "rent_period": "MONTHLY",
            "city": "Pune",
            "locality": "Viman Nagar",
            "address_line1": "Lane 5, Sakore Nagar, Viman Nagar",
            "state": "Maharashtra",
            "pincode": "411014",
            "gender_preference": "ANY",
            "furnished_status": "FURNISHED",
            "min_stay_months": 3,
            "max_occupancy": 2,
            "amenity_ids": [1, 2, 3, 4, 7]
        }
        create_res = client.post("/listings", json=listing_payload, headers=landlord_headers)
        print(f"[5] Create Listing: {create_res.status_code}")
        assert create_res.status_code == 201
        listing_data = create_res.json()["data"]
        listing_id = listing_data["id"]
        print(f"    Listing ID: {listing_id}")

        # Step 6: Upload photo 1 (house_listing_1.jpg) as cover
        img1_path = os.path.join(ASSETS_DIR, "house_listing_1.jpg")
        with open(img1_path, "rb") as f:
            upload1_res = client.post(
                f"/listings/{listing_id}/photos?is_cover=true&sort_order=0",
                files={"file": ("house_listing_1.jpg", f, "image/jpeg")},
                headers=landlord_headers
            )
        print(f"[6] Upload Photo 1 (Cover): {upload1_res.status_code}")
        assert upload1_res.status_code == 201
        photo1_data = upload1_res.json()["data"]
        print(f"    Photo 1 URL: {photo1_data['url']}")
        print(f"    Is Cover: {photo1_data['is_cover']}")

        # Step 7: Upload photo 2 (house_listing_2.jpg)
        img2_path = os.path.join(ASSETS_DIR, "house_listing_2.jpg")
        with open(img2_path, "rb") as f:
            upload2_res = client.post(
                f"/listings/{listing_id}/photos?is_cover=false&sort_order=1",
                files={"file": ("house_listing_2.jpg", f, "image/jpeg")},
                headers=landlord_headers
            )
        print(f"[7] Upload Photo 2: {upload2_res.status_code}")
        assert upload2_res.status_code == 201
        photo2_data = upload2_res.json()["data"]
        print(f"    Photo 2 URL: {photo2_data['url']}")

        # Step 8: Upload photo 3 (house_listing_3.jpg)
        img3_path = os.path.join(ASSETS_DIR, "house_listing_3.jpg")
        with open(img3_path, "rb") as f:
            upload3_res = client.post(
                f"/listings/{listing_id}/photos?is_cover=false&sort_order=2",
                files={"file": ("house_listing_3.jpg", f, "image/jpeg")},
                headers=landlord_headers
            )
        print(f"[8] Upload Photo 3: {upload3_res.status_code}")
        assert upload3_res.status_code == 201
        photo3_data = upload3_res.json()["data"]
        print(f"    Photo 3 ID: {photo3_data['id']}, URL: {photo3_data['url']}")

        # Step 9: Verify Listing Detail has all 3 photos
        detail_res = client.get(f"/listings/{listing_id}")
        print(f"[9] Get Listing Detail: {detail_res.status_code}")
        assert detail_res.status_code == 200
        photos_in_listing = detail_res.json()["data"]["photos"]
        print(f"    Total photos attached: {len(photos_in_listing)}")
        assert len(photos_in_listing) == 3

        # Step 10: Unhappy Path 1 - Student tries to upload photo (RBAC)
        with open(img1_path, "rb") as f:
            unhappy_student = client.post(
                f"/listings/{listing_id}/photos",
                files={"file": ("house_listing_1.jpg", f, "image/jpeg")},
                headers=student_headers
            )
        print(f"[10] Unhappy Path 1 (Student upload forbidden): {unhappy_student.status_code}")
        assert unhappy_student.status_code == 403
        print(f"     Error: {unhappy_student.json()['error']['code']}")

        # Step 11: Unhappy Path 2 - Unauthenticated upload
        with open(img1_path, "rb") as f:
            unhappy_unauth = client.post(
                f"/listings/{listing_id}/photos",
                files={"file": ("house_listing_1.jpg", f, "image/jpeg")}
            )
        print(f"[11] Unhappy Path 2 (Unauthenticated upload): {unhappy_unauth.status_code}")
        assert unhappy_unauth.status_code == 401
        print(f"     Error: {unhappy_unauth.json()['error']['code']}")

        # Step 12: Unhappy Path 3 - Non-existent listing ID
        with open(img1_path, "rb") as f:
            unhappy_notfound = client.post(
                "/listings/00000000-0000-0000-0000-000000000000/photos",
                files={"file": ("house_listing_1.jpg", f, "image/jpeg")},
                headers=landlord_headers
            )
        print(f"[12] Unhappy Path 3 (Non-existent listing): {unhappy_notfound.status_code}")
        assert unhappy_notfound.status_code == 404
        print(f"     Error: {unhappy_notfound.json()['error']['code']}")

        # Step 13: Admin approves listing
        approve_res = client.put(f"/admin/listings/{listing_id}/approve", headers=admin_headers)
        print(f"[13] Admin Approve Listing: {approve_res.status_code}")
        assert approve_res.status_code == 200
        assert approve_res.json()["data"]["status"] == "ACTIVE"

        # Step 14: Public Search returns approved listing with photo
        search_res = client.get("/listings?city=Pune")
        print(f"[14] Public Search: {search_res.status_code}")
        assert search_res.status_code == 200
        found = [l for l in search_res.json()["data"] if l["id"] == listing_id]
        assert len(found) == 1
        print(f"     Found active listing '{found[0]['title']}' with {len(found[0]['photos'])} photos.")

        # Step 15: Delete photo 3
        del_res = client.delete(f"/listings/{listing_id}/photos/{photo3_data['id']}", headers=landlord_headers)
        print(f"[15] Delete Photo 3: {del_res.status_code} - {del_res.json()}")
        assert del_res.status_code == 200

        # Step 16: Check Detail has 2 photos left
        final_detail = client.get(f"/listings/{listing_id}")
        remaining = final_detail.json()["data"]["photos"]
        print(f"[16] Remaining Photos in Listing: {len(remaining)}")
        assert len(remaining) == 2

        print("=" * 60)
        print("ALL API TESTS PASSED SUCCESSFULLY! (16/16 Checks)")
        print("=" * 60)

if __name__ == "__main__":
    run_tests()
