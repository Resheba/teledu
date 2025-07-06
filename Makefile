.SILENT:
.PHONY: init requirements run test build


init:
	POETRY_VIRTUALENVS_IN_PROJECT=true env -u VIRTUAL_ENV poetry install --no-root
	pre-commit install

requirements:
	poetry export -f requirements.txt -o requirements.txt --without-hashes --without-urls
	poetry export -f requirements.txt -o dev-requirements.txt --with=dev --without-hashes --without-urls

run:
	python -m src.main

test:
	mkdir -p report/tests/
	pytest --cov=src --html=report/tests/index.html tests/
	coverage html -d report/coverage

build:
	docker build -t teledu .

docker-run:
	docker run --rm --name=teledu -v "D:\SubLine\teledu\base.sql:\code\base.sql" --env-file=.env teledu
