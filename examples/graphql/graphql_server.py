#!/usr/bin/env python3
"""
GraphQL UserService server implemented with Strawberry + Flask.

The schema is derived entirely from Python type annotations.
Strawberry automatically converts snake_case Python field names to
camelCase GraphQL field names (e.g. user_id -> userId).

Run:
    python graphql_server.py

GraphiQL playground is available at:
    http://localhost:4000/graphql

Dependencies:
    pip install strawberry-graphql flask
"""

from __future__ import annotations

from typing import List, Optional

import strawberry
from flask import Flask
from strawberry.flask.views import GraphQLView

# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------
USERS_DB: dict[int, dict] = {
    42: dict(user_id="42", username="jdupont",
             email="j.dupont@example.com", role="editor",
             created_at="2024-03-15T10:30:00Z"),
    43: dict(user_id="43", username="mmartin",
             email="m.martin@example.com", role="viewer",
             created_at="2026-02-24T09:00:00Z"),
}
POSTS_DB: dict[int, list] = {
    42: [
        dict(post_id="1", title="Introduction to Distributed Systems",
             published_at="2026-01-10T08:00:00Z"),
        dict(post_id="2", title="Comparing API Paradigms",
             published_at="2026-02-01T14:30:00Z"),
    ]
}
_next_user_id: int = 44


# ---------------------------------------------------------------------------
# GraphQL types
# ---------------------------------------------------------------------------

@strawberry.type
class Post:
    post_id:      strawberry.ID
    title:        str
    published_at: str


@strawberry.type
class User:
    user_id:    strawberry.ID
    username:   str
    email:      str
    role:       str
    created_at: str

    @strawberry.field
    def posts(self) -> List[Post]:
        return [Post(**p) for p in POSTS_DB.get(int(self.user_id), [])]


# ---------------------------------------------------------------------------
# Root Query
# ---------------------------------------------------------------------------

@strawberry.type
class Query:

    @strawberry.field
    def user(self, user_id: strawberry.ID) -> Optional[User]:
        data = USERS_DB.get(int(user_id))
        return User(**data) if data else None

    @strawberry.field
    def users(self) -> List[User]:
        return [User(**d) for d in USERS_DB.values()]


# ---------------------------------------------------------------------------
# Root Mutation
# ---------------------------------------------------------------------------

@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_user(self, username: str, email: str, role: str) -> User:
        global _next_user_id
        data = dict(user_id=str(_next_user_id), username=username,
                    email=email, role=role, created_at="2026-02-25T00:00:00Z")
        USERS_DB[_next_user_id] = data
        _next_user_id += 1
        return User(**data)


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema),
)

if __name__ == "__main__":
    print("GraphQL endpoint : http://localhost:4000/graphql")
    print("GraphiQL UI      : http://localhost:4000/graphql")
    app.run(host="0.0.0.0", port=4000, debug=False)
