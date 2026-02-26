#!/usr/bin/env python3
"""
gRPC UserService client.

Run generate_proto.py and grpc_server.py first:
    python generate_proto.py
    python grpc_server.py   # in a separate terminal

Then run this client:
    python grpc_client.py

Dependencies:
    pip install grpcio grpcio-tools
"""

import grpc
import user_service_pb2
import user_service_pb2_grpc

CHANNEL_ADDRESS = "localhost:50051"


# ---------------------------------------------------------------------------
# RPC wrappers
# ---------------------------------------------------------------------------

def get_user(user_id: int) -> None:
    """Unary call: retrieve one user by ID."""
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        try:
            resp = stub.GetUser(user_service_pb2.GetUserRequest(user_id=user_id))
            print(
                f"  GetUser({user_id}) -> "
                f"username={resp.username}, email={resp.email}, role={resp.role}"
            )
        except grpc.RpcError as exc:
            print(f"  GetUser({user_id}) -> RPC error: {exc.code()} - {exc.details()}")


def list_users() -> None:
    """Server-streaming call: iterate over all users returned by the server."""
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        print("  ListUsers stream:")
        for resp in stub.ListUsers(user_service_pb2.ListUsersRequest()):
            print(f"    [{resp.user_id}] {resp.username} <{resp.email}> ({resp.role})")


def create_user(username: str, email: str, role: str) -> int:
    """Unary call: create a user and return the assigned user_id."""
    with grpc.insecure_channel(CHANNEL_ADDRESS) as channel:
        stub = user_service_pb2_grpc.UserServiceStub(channel)
        resp = stub.CreateUser(
            user_service_pb2.CreateUserRequest(
                username=username,
                email=email,
                role=role,
            )
        )
        print(
            f"  CreateUser -> user_id={resp.user_id}, username={resp.username}"
        )
        return resp.user_id


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("--- GetUser (id=42) ---")
    get_user(42)

    print("\n--- GetUser (id=99, non-existent) ---")
    get_user(99)

    print("\n--- ListUsers (server-streaming) ---")
    list_users()

    print("\n--- CreateUser ---")
    new_id = create_user(
        username="lbernard",
        email="l.bernard@example.com",
        role="admin",
    )

    print("\n--- GetUser (newly created) ---")
    get_user(new_id)
