#!/usr/bin/env python3
"""
GraphQL UserService client using the requests library.

Sends queries and mutations to the Strawberry server as plain HTTP POST
requests with a JSON body.  No special GraphQL client library is needed.

Start the server first:
    python graphql_server.py

Then run this file:
    python graphql_client.py

Dependencies:
    pip install requests
"""

import json

import requests

ENDPOINT = "http://localhost:4000/graphql"


# ---------------------------------------------------------------------------
# Generic GraphQL executor
# ---------------------------------------------------------------------------

def gql(query: str, variables: dict | None = None) -> dict:
    """Execute a GraphQL operation and return the full response body."""
    payload: dict = {"query": query}
    if variables:
        payload["variables"] = variables
    response = requests.post(
        ENDPOINT,
        json=payload,
        headers={"Content-Type": "application/json"},
    )
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Defined operations
# ---------------------------------------------------------------------------

QUERY_USER_WITH_POSTS = """
  query GetUserWithPosts($id: ID!) {
    user(userId: $id) {
      username
      email
      posts {
        title
        publishedAt
      }
    }
  }
"""

QUERY_ALL_USERS = """
  query {
    users {
      userId
      username
      role
    }
  }
"""

MUTATION_CREATE_USER = """
  mutation CreateUser($username: String!, $email: String!, $role: String!) {
    createUser(username: $username, email: $email, role: $role) {
      userId
      username
      email
    }
  }
"""


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Query: user 42 with only username, email, and their post titles
    # (userId, role, createdAt are intentionally omitted from the selection)
    print("=== Query: GetUserWithPosts (id=42) ===")
    result = gql(QUERY_USER_WITH_POSTS, {"id": "42"})
    print(json.dumps(result, indent=2))

    # Query: all users, but only the three fields listed in the selection set
    print("\n=== Query: all users (userId + username + role only) ===")
    result = gql(QUERY_ALL_USERS)
    print(json.dumps(result, indent=2))

    # Mutation: create a new user
    print("\n=== Mutation: CreateUser ===")
    result = gql(
        MUTATION_CREATE_USER,
        {
            "username": "lbernard",
            "email":    "l.bernard@example.com",
            "role":     "admin",
        },
    )
    print(json.dumps(result, indent=2))
