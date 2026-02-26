PYTHON    := $(shell [ -f ../../.venv/bin/python ] && echo ../../.venv/bin/python || echo python3)
PORT      := 50051
LOGFILE   := /tmp/grpc_server.log
PROTO_OUT := user_service_pb2.py user_service_pb2_grpc.py

.DEFAULT_GOAL := help
.PHONY: help proto run test clean

help:
	@echo ""
	@echo "  gRPC UserService example  (port $(PORT))"
	@echo "  ──────────────────────────────────────────"
	@echo "  make proto  Generate Python bindings from user_service.proto"
	@echo "  make run    Generate bindings + start gRPC server (Ctrl-C to stop)"
	@echo "  make test   Generate bindings + start server + run client"
	@echo "  make clean  Remove generated bindings, pycache, and log files"
	@echo ""

# Generate pb2 files only when the .proto source is newer
user_service_pb2.py: user_service.proto
	@echo "==> [gRPC] Generating protobuf bindings from user_service.proto..."
	$(PYTHON) generate_proto.py

proto: user_service_pb2.py

run: proto
	@echo "==> [gRPC] Server listening on port $(PORT)"
	$(PYTHON) grpc_server.py

test: proto
	@echo ""
	@echo "==> [gRPC] Starting server on port $(PORT)..."
	@$(PYTHON) grpc_server.py > $(LOGFILE) 2>&1 & \
	SERVER_PID=$$!; \
	sleep 2; \
	echo "==> [gRPC] Running client..."; \
	echo ""; \
	$(PYTHON) grpc_client.py; \
	CLIENT_EXIT=$$?; \
	echo ""; \
	echo "==> [gRPC] Stopping server (PID $$SERVER_PID)"; \
	kill $$SERVER_PID 2>/dev/null; \
	exit $$CLIENT_EXIT

clean:
	rm -f $(PROTO_OUT) $(LOGFILE)
	rm -rf __pycache__
