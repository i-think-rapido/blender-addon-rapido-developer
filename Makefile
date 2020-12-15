.PHONY: clean virtualenv test docker dist dist-upload

clean:
	find . -name '*.py[co]' -delete
	rm -rf dist build

virtualenv:
	python -m venv --prompt '|> rapidodeveloper <| ' .venv
	.venv/bin/pip install -r requirements-dev.txt
	.venv/bin/python setup.py develop
	@echo
	@echo "VirtualENV Setup Complete. Now run: source .venv/bin/activate"
	@echo

test:
	python -m pytest \
		-v \
		--cov=rapidodeveloper \
		--cov-report=term \
		--cov-report=html:coverage-report \
		tests/

docker: clean
	docker build -t rapidodeveloper:latest .

dist: clean
	python setup.py sdist
	python setup.py bdist_wheel
	python .venv/bin/rapidodeveloper build-addon

dist-upload:
	twine upload dist/*
