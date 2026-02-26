#!/usr/bin/env python3
"""
gRPC UserService server.

Run generate_proto.py first to create user_service_pb2.py and
user_service_pb2_grpc.py, then start this server:

    python generate_proto.py
    python grpc_server.py

The server listens on port 50051.

Dependencies:
    pip install grpcio grpcio-tools
"""

from concurrent import futures

import grpc
import user_service_pb2
import user_service_pb2_grpc


# ---------------------------------------------------------------------------
# In-memory data store
# ---------------------------------------------------------------------------

USERS: dict[int, dict] = {
    42: dict(username="jdupont",  email="j.dupont@example.com",  role="editor"),
    43: dict(username="mmartin",  email="m.martin@example.com",  role="viewer"),
}

_next_id: int = 44


# ---------------------------------------------------------------------------
# Servicer implementation
# ---------------------------------------------------------------------------

class UserServiceServicer(user_service_pb2_grpc.UserServiceServicer):
    """Concrete implementation of the UserService gRPC service."""

    def GetUser(self, request, context):
        """Unary RPC: return the user with request.user_id."""
        user = USERS.get(request.user_id)
        if user is None:
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                f"User {request.user_id} not found.",
            )
        return user_service_pb2.UserResponse(
            user_id=request.user_id,
            username=user["username"],
            email=user["email"],
            role=user["role"],
        )

    def ListUsers(self, request, context):
        """Server-streaming RPC: yield one UserResponse per stored user."""
        for user_id, user in USERS.items():
            yield user_service_pb2.UserResponse(
                user_id=user_id,
                username=user["username"],
                email=user["email"],
                role=user["role"],
            )

    def CreateUser(self, request, context):
        """Unary RPC: persist a new user and return it."""
        global _next_id
        USERS[_next_id] = dict(
            username=request.username,
            email=request.email,
            role=request.role,
        )
        response = user_service_pb2.UserResponse(
            user_id=_next_id,
            username=request.username,
            email=request.email,
            role=request.role,
        )
        _next_id += 1
        return response


# ---------------------------------------------------------------------------
# Server bootstrap
# ---------------------------------------------------------------------------

def serve(port: int = 50051) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service_pb2_grpc.add_UserServiceServicer_to_server(
        UserServiceServicer(), server
    )
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print(f"gRPC server listening on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
