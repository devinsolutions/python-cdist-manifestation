.PHONY: install lint

all: install lint test

install:
	pip install -e .[test]

lint:
	flake8
