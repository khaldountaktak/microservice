PYTHON  := $(shell [ -f ../../.venv/bin/python ] && echo ../../.venv/bin/python || echo python3)
PORT    := 4000
LOGFILE := /tmp/graphql_server.log

.DEFAULT_GOAL := help
.PHONY: help run test clean

help:
	@echo ""
	@echo "  GraphQL UserService example  (port $(PORT))"
	@echo "  ─────────────────────────────────────────────"
	@echo "  make run    Start the GraphQL server in the foreground (Ctrl-C to stop)"
	@echo "  make test   Start server + run client automatically, then stop server"
	@echo "  make clean  Remove temporary log files"
	@echo ""

run:
	@echo "==> GraphQL server  →  http://localhost:$(PORT)/graphql"
	@echo "==> GraphiQL UI     →  http://localhost:$(PORT)/graphql  (browser)"
	$(PYTHON) graphql_server.py

test:
	@echo ""
	@echo "==> [GraphQL] Starting server on port $(PORT)..."
	@$(PYTHON) graphql_server.py > $(LOGFILE) 2>&1 & \
	SERVER_PID=$$!; \
	sleep 2; \
	echo "==> [GraphQL] Running client..."; \
	echo ""; \
	$(PYTHON) graphql_client.py; \
	CLIENT_EXIT=$$?; \
	echo ""; \
	echo "==> [GraphQL] Stopping server (PID $$SERVER_PID)"; \
	kill $$SERVER_PID 2>/dev/null; \
	exit $$CLIENT_EXIT

clean:
	rm -f $(LOGFILE)
