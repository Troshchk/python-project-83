build-p:
	poetry build

publish:
	poetry publish --dry-run

lint:
	poetry run flake8 page_analyzer

install:
	poetry install

test-coverage:
	poetry run pytest --cov=page_analyzer --cov-report xml

local-test-coverage:
	poetry run pytest --cov=page_analyzer

dev:
	poetry run flask --app page_analyzer:app --debug run --port 8000

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

build:
	./build.sh
