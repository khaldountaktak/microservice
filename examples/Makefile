PYTHON := $(shell [ -f ../.venv/bin/python ] && echo ../.venv/bin/python || echo python3)

.DEFAULT_GOAL := help
.PHONY: help install test-soap test-rest test-graphql test-grpc test-all clean-all

help:
	@echo ""
	@echo "  API paradigms — examples"
	@echo "  ─────────────────────────────────────────────────────"
	@echo "  make install        Install all dependencies into the venv"
	@echo "  make test-soap      Test the SOAP example"
	@echo "  make test-rest      Test the REST example"
	@echo "  make test-graphql   Test the GraphQL example"
	@echo "  make test-grpc      Test the gRPC example (generates bindings first)"
	@echo "  make test-all       Run all four tests in sequence"
	@echo "  make clean-all      Clean generated and temporary files in all examples"
	@echo ""

install:
	@echo "==> Installing dependencies from requirements.txt..."
	$(PYTHON) -m pip install -r requirements.txt

test-soap:
	@$(MAKE) -C soap test

test-rest:
	@$(MAKE) -C rest test

test-graphql:
	@$(MAKE) -C graphql test

test-grpc:
	@$(MAKE) -C grpc test

test-all: test-soap test-rest test-graphql test-grpc
	@echo ""
	@echo "  ✓  All four examples passed."
	@echo ""

clean-all:
	@$(MAKE) -C soap clean
	@$(MAKE) -C rest clean
	@$(MAKE) -C graphql clean
	@$(MAKE) -C grpc clean
	@echo "==> Cleaned."
