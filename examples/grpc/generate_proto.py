#!/usr/bin/env python3
"""
Generate Python bindings from user_service.proto.

This script invokes the protoc compiler through the grpcio-tools package
and produces two files in the same directory:

    user_service_pb2.py       -- message classes (serialisation / deserialisation)
    user_service_pb2_grpc.py  -- service stub and servicer base classes

Run this once before starting the server or client:
    python generate_proto.py

Dependencies:
    pip install grpcio grpcio-tools
"""

import subprocess
import sys
from pathlib import Path

PROTO_FILE = Path(__file__).parent / "user_service.proto"
OUT_DIR    = Path(__file__).parent

result = subprocess.run(
    [
        sys.executable,
        "-m", "grpc_tools.protoc",
        f"--proto_path={PROTO_FILE.parent}",
        f"--python_out={OUT_DIR}",
        f"--grpc_python_out={OUT_DIR}",
        str(PROTO_FILE),
    ],
    check=True,
)

print("Generated successfully:")
print(f"  {OUT_DIR / 'user_service_pb2.py'}")
print(f"  {OUT_DIR / 'user_service_pb2_grpc.py'}")
