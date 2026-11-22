PYTHON ?= python

.PHONY: data experiments figures all quick test animations animations-final
data:
	$(PYTHON) -m src.cli data
experiments:
	$(PYTHON) -m src.cli experiments
figures:
	$(PYTHON) -m src.cli figures
all:
	$(PYTHON) -m src.cli all
quick:
	$(PYTHON) -m src.cli all --quick
test:
	$(PYTHON) -m pytest
animations:
	bash animations/render_all.sh preview
animations-final:
	bash animations/render_all.sh final

