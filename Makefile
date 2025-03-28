
default: all
all: run
# python stuff

BIN = ./.venv/bin
SRC = ./src/*.py
# bootstrap:
# 	python -m venv venv
# 	./venv/bin/python -m pip install uv
install: clean
	uv venv --python=/usr/bin/python
	uv pip install -r requirements.txt

run: format
	./src/main.py

format:
	$(BIN)/ruff format

lint:
	$(BIN)/ruff check

typecheck:
	$(BIN)/mypy $(SRC)

test: format typecheck
	pytest $(SRC)

clean:
	rm -f ./*.{o,elf,s,uf2,ss,dump}
	rm -rf ./{venv,.venv}