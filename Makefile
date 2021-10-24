.PHONY: check-style unit-test

check-style:
	black --check gdeplop
	flake8

unit-test:
	poetry run pytest
