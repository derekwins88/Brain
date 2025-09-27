.PHONY: docs serve clean notes-setup notes-diagram notes-docs

# Versions pinned for reproducibility
MDBOOK_VER := 0.4.40
MERMAID_VER := 0.13.0
SITEMAP_VER := 0.7.0

_install_docs_tools:
	cargo install mdbook --version $(MDBOOK_VER) --locked || true
	cargo install mdbook-mermaid --version $(MERMAID_VER) --locked || true
	# sitemap is optional; install if book.toml requests it
	grep -q 'preprocessor.sitemap' book.toml && cargo install mdbook-sitemap --version $(SITEMAP_VER) --locked || true || true

docs:
	$(MAKE) _install_docs_tools
	mdbook build

serve:
	$(MAKE) _install_docs_tools
	mdbook serve -n 127.0.0.1 -p 3000

clean:
	rm -rf book

# Compatibility targets used by another workflow you showed
notes-setup:
	$(MAKE) _install_docs_tools

notes-diagram:
	@echo "Diagrams rendered by mdbook-mermaid during build"

notes-docs: notes-setup
	mdbook build
