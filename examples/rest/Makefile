PYTHON  := $(shell [ -f ../../.venv/bin/python ] && echo ../../.venv/bin/python || echo python3)
PORT    := 5000
LOGFILE := /tmp/rest_server.log

.DEFAULT_GOAL := help
.PHONY: help run test clean

help:
	@echo ""
	@echo "  REST UserService example  (port $(PORT))"
	@echo "  ─────────────────────────────────────────"
	@echo "  make run    Start the REST server in the foreground (Ctrl-C to stop)"
	@echo "  make test   Start server + run client automatically, then stop server"
	@echo "  make clean  Remove temporary log files"
	@echo ""

run:
	@echo "==> REST server  →  http://localhost:$(PORT)/api/users"
	$(PYTHON) rest_server.py

test:
	@echo ""
	@echo "==> [REST] Starting server on port $(PORT)..."
	@$(PYTHON) rest_server.py > $(LOGFILE) 2>&1 & \
	SERVER_PID=$$!; \
	sleep 2; \
	echo "==> [REST] Running client..."; \
	echo ""; \
	$(PYTHON) rest_client.py; \
	CLIENT_EXIT=$$?; \
	echo ""; \
	echo "==> [REST] Stopping server (PID $$SERVER_PID)"; \
	kill $$SERVER_PID 2>/dev/null; \
	exit $$CLIENT_EXIT

clean:
	rm -f $(LOGFILE)
