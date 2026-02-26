PYTHON  := $(shell [ -f ../../.venv/bin/python ] && echo ../../.venv/bin/python || echo python3)
PORT    := 8000
LOGFILE := /tmp/soap_server.log

.DEFAULT_GOAL := help
.PHONY: help run test clean

help:
	@echo ""
	@echo "  SOAP UserService example  (port $(PORT))"
	@echo "  ─────────────────────────────────────────"
	@echo "  make run    Start the SOAP server in the foreground (Ctrl-C to stop)"
	@echo "  make test   Start server + run client automatically, then stop server"
	@echo "  make clean  Remove temporary log files"
	@echo ""

run:
	@echo "==> SOAP server  →  http://localhost:$(PORT)/userservice"
	@echo "==>              →  http://localhost:$(PORT)/userservice?wsdl"
	$(PYTHON) soap_server.py

test:
	@echo ""
	@echo "==> [SOAP] Starting server on port $(PORT)..."
	@$(PYTHON) soap_server.py > $(LOGFILE) 2>&1 & \
	SERVER_PID=$$!; \
	sleep 2; \
	echo "==> [SOAP] Running client..."; \
	echo ""; \
	$(PYTHON) soap_client.py; \
	CLIENT_EXIT=$$?; \
	echo ""; \
	echo "==> [SOAP] Stopping server (PID $$SERVER_PID)"; \
	kill $$SERVER_PID 2>/dev/null; \
	exit $$CLIENT_EXIT

clean:
	rm -f $(LOGFILE)
