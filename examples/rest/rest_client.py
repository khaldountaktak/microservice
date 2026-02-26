#!/usr/bin/env python3
"""
RESTful UserService client using the requests library.

Demonstrates all five CRUD operations against the Flask server.

Start the server first:
    python rest_server.py

Then run this file:
    python rest_client.py

Dependencies:
    pip install requests
"""

import json

import requests

BASE_URL = "http://localhost:5000/api"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def print_response(resp: requests.Response) -> None:
    print(f"  HTTP {resp.status_code}")
    if resp.content:
        print(f"  {json.dumps(resp.json(), indent=2)}")


# ---------------------------------------------------------------------------
# Operations
# ---------------------------------------------------------------------------

def list_users() -> None:
    print("--- GET /api/users ---")
    resp = requests.get(f"{BASE_URL}/users")
    print_response(resp)


def get_user(user_id: int) -> None:
    print(f"\n--- GET /api/users/{user_id} ---")
    resp = requests.get(f"{BASE_URL}/users/{user_id}")
    print_response(resp)


def create_user(username: str, email: str, role: str) -> int:
    """Create a user and return the newly assigned user_id."""
    print("\n--- POST /api/users ---")
    resp = requests.post(
        f"{BASE_URL}/users",
        json={"username": username, "email": email, "role": role},
    )
    print_response(resp)
    if resp.status_code == 201:
        print(f"  Location: {resp.headers.get('Location')}")
    return resp.json().get("user_id", -1)


def update_user(user_id: int, **fields) -> None:
    print(f"\n--- PATCH /api/users/{user_id} ---")
    resp = requests.patch(f"{BASE_URL}/users/{user_id}", json=fields)
    print_response(resp)


def delete_user(user_id: int) -> None:
    print(f"\n--- DELETE /api/users/{user_id} ---")
    resp = requests.delete(f"{BASE_URL}/users/{user_id}")
    print(f"  HTTP {resp.status_code}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # List the two seed users
    list_users()

    # Read one by ID
    get_user(42)

    # Attempt to read a non-existent user
    get_user(99)

    # Create a new user
    new_id = create_user(
        username="lbernard",
        email="l.bernard@example.com",
        role="admin",
    )

    # Partially update its role
    update_user(new_id, role="editor")

    # Delete it
    delete_user(new_id)

    # Confirm deletion: list again to verify
    list_users()
