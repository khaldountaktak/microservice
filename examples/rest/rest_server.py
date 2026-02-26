#!/usr/bin/env python3
"""
RESTful UserService server implemented with Flask.

Exposes a standard CRUD interface for user resources over HTTP, following
REST constraints: stateless server, resource-oriented URIs, HTTP verbs for
semantics, and standard status codes for outcomes.

Run:
    python rest_server.py

Endpoints:
    GET    /api/users           List all users
    GET    /api/users/<id>      Retrieve a user by ID
    POST   /api/users           Create a new user
    PATCH  /api/users/<id>      Partially update a user
    DELETE /api/users/<id>      Delete a user

Dependencies:
    pip install flask
"""

from datetime import datetime, timezone

from flask import Flask, Response, abort, jsonify, request

app = Flask(__name__)


# ---------------------------------------------------------------------------
# In-memory store
# ---------------------------------------------------------------------------

USERS: dict[int, dict] = {
    42: {
        "user_id":    42,
        "username":   "jdupont",
        "email":      "j.dupont@example.com",
        "role":       "editor",
        "created_at": "2024-03-15T10:30:00Z",
    },
    43: {
        "user_id":    43,
        "username":   "mmartin",
        "email":      "m.martin@example.com",
        "role":       "viewer",
        "created_at": "2026-02-24T09:00:00Z",
    },
}

_next_id: int = 44


def _now() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/users")
def list_users():
    """Return all user records as a JSON array."""
    return jsonify(list(USERS.values())), 200


@app.get("/api/users/<int:user_id>")
def get_user(user_id: int):
    """Return a single user by primary key."""
    user = USERS.get(user_id)
    if user is None:
        abort(404, description=f"User {user_id} not found.")
    return jsonify(user), 200


@app.post("/api/users")
def create_user():
    """Create a new user.  Required body fields: username, email, role."""
    global _next_id
    body = request.get_json(force=True, silent=True) or {}
    for required_field in ("username", "email", "role"):
        if required_field not in body:
            abort(400, description=f"Missing required field: '{required_field}'.")
    user = {
        "user_id":    _next_id,
        "username":   body["username"],
        "email":      body["email"],
        "role":       body["role"],
        "created_at": _now(),
    }
    USERS[_next_id] = user
    _next_id += 1
    response = jsonify(user)
    response.status_code = 201
    response.headers["Location"] = f"/api/users/{user['user_id']}"
    return response


@app.patch("/api/users/<int:user_id>")
def update_user(user_id: int):
    """Partially update a user.  Only the fields present in the body are changed."""
    user = USERS.get(user_id)
    if user is None:
        abort(404, description=f"User {user_id} not found.")
    body = request.get_json(force=True, silent=True) or {}
    for field in ("username", "email", "role"):
        if field in body:
            user[field] = body[field]
    return jsonify(user), 200


@app.delete("/api/users/<int:user_id>")
def delete_user(user_id: int):
    """Delete a user.  Returns 204 No Content on success."""
    if user_id not in USERS:
        abort(404, description=f"User {user_id} not found.")
    del USERS[user_id]
    return Response(status=204)


# ---------------------------------------------------------------------------
# Error handlers: always respond with a JSON body
# ---------------------------------------------------------------------------

@app.errorhandler(400)
@app.errorhandler(404)
def handle_http_error(error):
    return jsonify({"error": str(error.description)}), error.code


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
