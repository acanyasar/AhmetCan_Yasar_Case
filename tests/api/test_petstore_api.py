"""
PetStore API Tests — CRUD Operations
======================================
Base URL: https://petstore.swagger.io/v2

Covers:
  Positive:
    - Create a pet (POST /pet)
    - Read a pet by ID (GET /pet/{id})
    - Update a pet (PUT /pet)
    - Delete a pet (DELETE /pet/{id})

  Negative:
    - Get a non-existent pet (GET /pet/{id}) → 404
    - Create a pet with an invalid/empty body → 4xx/5xx
    - Delete a non-existent pet → 404
    - Get a pet with an invalid (string) ID → 4xx

Run:
    pytest tests/api/ -v
"""

import pytest
import requests
import time

BASE_URL = "https://petstore.swagger.io/v2"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# A unique pet ID to avoid collisions with concurrent Swagger demo users
PET_ID = int(time.time()) % 10_000_000 + 900_000


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def created_pet_id():
    """
    Creates a pet before the positive test suite and yields its ID.
    The pet is deleted after all module tests complete.
    """
    payload = {
        "id": PET_ID,
        "category": {"id": 1, "name": "Dogs"},
        "name": "TestDoggie",
        "photoUrls": ["https://example.com/dog.png"],
        "tags": [{"id": 1, "name": "test-tag"}],
        "status": "available",
    }
    response = requests.post(f"{BASE_URL}/pet", json=payload, headers=HEADERS)
    assert response.status_code == 200, f"Setup failed: {response.text}"
    yield PET_ID
    # Teardown — best-effort delete
    requests.delete(f"{BASE_URL}/pet/{PET_ID}", headers=HEADERS)


# ── Positive Tests ────────────────────────────────────────────────────────────

@pytest.mark.api
class TestPetCRUDPositive:
    """Happy-path CRUD operations on /pet endpoints."""

    def test_create_pet(self):
        """POST /pet — creates a new pet and returns the created resource."""
        unique_id = PET_ID + 1
        payload = {
            "id": unique_id,
            "category": {"id": 2, "name": "Cats"},
            "name": "WhiskersCat",
            "photoUrls": ["https://example.com/cat.png"],
            "tags": [{"id": 2, "name": "cat-tag"}],
            "status": "available",
        }
        response = requests.post(f"{BASE_URL}/pet", json=payload, headers=HEADERS)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert body["id"] == unique_id
        assert body["name"] == "WhiskersCat"
        assert body["status"] == "available"

        # Cleanup
        requests.delete(f"{BASE_URL}/pet/{unique_id}", headers=HEADERS)

    def test_get_pet(self, created_pet_id):
        """GET /pet/{id} — retrieves the pet created in the fixture."""
        response = requests.get(f"{BASE_URL}/pet/{created_pet_id}", headers=HEADERS)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert body["id"] == created_pet_id
        assert body["name"] == "TestDoggie"

    def test_update_pet(self, created_pet_id):
        """PUT /pet — updates an existing pet's name and status."""
        payload = {
            "id": created_pet_id,
            "category": {"id": 1, "name": "Dogs"},
            "name": "UpdatedDoggie",
            "photoUrls": ["https://example.com/dog.png"],
            "tags": [{"id": 1, "name": "test-tag"}],
            "status": "sold",
        }
        response = requests.put(f"{BASE_URL}/pet", json=payload, headers=HEADERS)

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert body["name"] == "UpdatedDoggie"
        assert body["status"] == "sold"

    def test_delete_pet(self, created_pet_id):
        """DELETE /pet/{id} — deletes an existing pet successfully."""
        response = requests.delete(
            f"{BASE_URL}/pet/{created_pet_id}", headers=HEADERS
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )

    def test_get_pets_by_status_available(self):
        """GET /pet/findByStatus — retrieves pets with status 'available'."""
        response = requests.get(
            f"{BASE_URL}/pet/findByStatus",
            params={"status": "available"},
            headers=HEADERS,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert isinstance(body, list), "Response should be a list of pets"
        assert len(body) > 0, "Expected at least one pet with status 'available'"
        for pet in body:
            assert pet.get("status") == "available", (
                f"Pet {pet.get('id')} has status '{pet.get('status')}' instead of 'available'"
            )

    def test_get_pets_by_status_sold(self):
        """GET /pet/findByStatus — retrieves pets with status 'sold'."""
        response = requests.get(
            f"{BASE_URL}/pet/findByStatus",
            params={"status": "sold"},
            headers=HEADERS,
        )

        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}: {response.text}"
        )
        body = response.json()
        assert isinstance(body, list)


# ── Negative Tests ────────────────────────────────────────────────────────────

@pytest.mark.api
class TestPetCRUDNegative:
    """Error and edge-case scenarios for /pet endpoints."""

    NON_EXISTENT_ID = 9999999999

    def test_get_nonexistent_pet(self):
        """GET /pet/{id} with an ID that does not exist → 404."""
        response = requests.get(
            f"{BASE_URL}/pet/{self.NON_EXISTENT_ID}", headers=HEADERS
        )

        assert response.status_code == 404, (
            f"Expected 404 for non-existent pet, got {response.status_code}"
        )

    def test_delete_nonexistent_pet(self):
        """DELETE /pet/{id} with a non-existent ID → 404."""
        response = requests.delete(
            f"{BASE_URL}/pet/{self.NON_EXISTENT_ID}", headers=HEADERS
        )

        assert response.status_code == 404, (
            f"Expected 404 when deleting non-existent pet, got {response.status_code}"
        )

    def test_get_pet_invalid_id_string(self):
        """GET /pet/{id} with a non-numeric ID (string) → 400 or 404."""
        response = requests.get(f"{BASE_URL}/pet/not-a-valid-id", headers=HEADERS)

        assert response.status_code in (400, 404), (
            f"Expected 400 or 404 for invalid pet ID, got {response.status_code}"
        )

    def test_create_pet_missing_required_fields(self):
        """
        POST /pet with an empty JSON body.
        Petstore returns 405 (Method Not Allowed / Validation Error) for bad input.
        """
        response = requests.post(f"{BASE_URL}/pet", json={}, headers=HEADERS)

        assert response.status_code in (400, 405, 422, 500), (
            f"Expected a client/server error for empty pet body, "
            f"got {response.status_code}: {response.text}"
        )

    def test_create_pet_invalid_json(self):
        """POST /pet with plain text instead of JSON → 4xx or 5xx."""
        response = requests.post(
            f"{BASE_URL}/pet",
            data="this is not json",
            headers={"Content-Type": "application/json"},
        )

        assert response.status_code >= 400, (
            f"Expected error for invalid JSON body, got {response.status_code}"
        )

    def test_update_nonexistent_pet(self):
        """
        PUT /pet with an ID that does not exist.
        Petstore may return 200 (upsert) or 404 — we verify no 5xx.
        """
        payload = {
            "id": self.NON_EXISTENT_ID,
            "name": "GhostPet",
            "photoUrls": [],
            "status": "available",
        }
        response = requests.put(f"{BASE_URL}/pet", json=payload, headers=HEADERS)

        assert response.status_code < 500, (
            f"Server error on update of non-existent pet: {response.status_code}"
        )

    def test_get_pets_by_invalid_status(self):
        """GET /pet/findByStatus with an invalid status value → 400."""
        response = requests.get(
            f"{BASE_URL}/pet/findByStatus",
            params={"status": "nonexistent_status"},
            headers=HEADERS,
        )

        # Swagger petstore returns 400 for unknown status
        assert response.status_code == 400, (
            f"Expected 400 for invalid status filter, got {response.status_code}"
        )
