.PHONY: docs serve clean

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
