.PHONY: sync build clean

sync:
	.github/scripts/sync_toolchain.sh lean

build: sync
	cd lean && lake update && lake build

clean:
	rm -rf lean/.lake lean/build
