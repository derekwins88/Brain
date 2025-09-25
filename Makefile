.PHONY: sync build clean

sync:
	.github/scripts/sync_toolchain.sh lean

build: sync
	cd lean && lake update && lake build

clean:
	rm -rf lean/.lake lean/build
render-day3:
	python -m nbconvert --to notebook --execute \
	  notebooks/render_infographic.ipynb \
	  --output /tmp/render_local.ipynb
	@echo "PNG at docs/day3_infographic.png"

render-day3-smoke:
	SMOKE=1 python -m nbconvert --to notebook --execute \
	  notebooks/render_infographic.ipynb \
	  --output /tmp/render_smoke.ipynb
	@echo "SMOKE PNG at docs/day3_infographic.png"

### Notes/Docs heartbeat (additive targets)
SHELL := /bin/bash
NODE_BIN ?= ./node_modules/.bin
MERMAID ?= $(NODE_BIN)/mmdc
PANDOC ?= pandoc

.PHONY: notes-setup notes-diagram notes-docs notes-clean

notes-setup:
	@npm -s init -y >/dev/null 2>&1 || true
	@npm -s i @mermaid-js/mermaid-cli@10 --save-dev

notes-diagram:
	@mkdir -p docs/diagrams
	@test -x $(MERMAID) || (echo "Mermaid CLI missing. Run: make notes-setup" && exit 1)
	@$(MERMAID) -i notes/system.mmd -o docs/diagrams/system.svg

notes-docs:
	@mkdir -p docs
	@which $(PANDOC) >/dev/null || (echo "Pandoc not found. Install pandoc." && exit 1)
	@$(PANDOC) notes/index.md -o docs/Brain.pdf

notes-clean:
	@rm -f docs/Brain.pdf docs/diagrams/system.svg
