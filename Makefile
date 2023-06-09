update-precommit:
	poetry run pre-commit autoupdate

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx
