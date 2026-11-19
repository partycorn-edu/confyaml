PYTHON ?= python3
export PYTHONPATH := src

.PHONY: install run test

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m confyaml

test:
	$(PYTHON) -m unittest discover -s tests -v
