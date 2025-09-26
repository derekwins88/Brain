.PHONY: docs serve clean notes-setup notes-diagram notes-docs

# --- mdBook core ---
docs:
	cargo install mdbook --version 0.4.40 --locked || true
	cargo install mdbook-mermaid --version 0.13.0 --locked || true
	mdbook build

serve:
	cargo install mdbook --version 0.4.40 --locked || true
	cargo install mdbook-mermaid --version 0.13.0 --locked || true
	mdbook serve -n 127.0.0.1 -p 3000

clean:
	rm -rf book

# --- Notes pipeline compatibility (what your CI calls) ---
notes-setup:
	cargo install mdbook --version 0.4.40 --locked || true
	cargo install mdbook-mermaid --version 0.13.0 --locked || true

# If you later render standalone diagrams, hook it here.
# For now, let mdBook-mermaid handle diagrams during build.
notes-diagram:
	@echo "notes-diagram: handled by mdBook-mermaid during build"

notes-docs: notes-setup
	mdbook build
