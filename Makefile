install:
	poetry install
dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000
lint:
	poetry run flake8 page_analyzer
test:
	poetry run pytest -vv
selfcheck:
	poetry check
check: selfcheck test lint

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app