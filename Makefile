# civmatflow v2 — developer targets
PY ?= python3
DST ?= $(HOME)/.claude
PROJECT ?= $(PWD)

.PHONY: test lint install help

help:
	@echo "make test                      offline smoke test of all tools"
	@echo "make lint                      syntax checks (python, bash, workflow scripts)"
	@echo "make install DST=~/.claude PROJECT=~/research/0970project"

test:
	CIVMAT2_PYTHON=$(PY) bash tests/smoke_test.sh

lint:
	@for f in tools/*.py style/*/style_check.py; do $(PY) -m py_compile $$f; done
	@for f in bin/civmat2 install.sh codex/run_iter.sh tests/smoke_test.sh templates/run_all.sh; do bash -n $$f; done
	@if command -v node >/dev/null; then for f in workflows/*.js; do \
	  { echo 'async function __wf(args, agent, parallel, pipeline, phase, log) {'; sed 's/^export const meta/const meta/' $$f; echo '}'; } | node --input-type=module --check || exit 1; done; fi
	@! grep -rn "/home/luck\|~/xzy" skills agents workflows codex tools bin templates tests install.sh || (echo "absolute paths found"; exit 1)
	@echo "lint OK"

install:
	./install.sh $(DST) --project $(PROJECT) --python $(PY)
