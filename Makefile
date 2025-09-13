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
