all: clean-pyc test

test:
	python setup.py nosetests --tests tests/runtests.py

travis:
	python setup.py nosetests --tests tests/runtests.py

coverage:
	python setup.py nosetests  --with-coverage --cover-package=jinja_kit --cover-html --cover-html-dir=coverage_out coverage


shell:
	../venv/bin/ipython

audit:
	python setup.py autdit

dist:
	python setup.py sdist

release:
	python setup.py sdist upload

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

find-print:
	grep -r --include=*.py --exclude-dir=venv --exclude=fabfile* --exclude=tests.py --exclude-dir=tests --exclude-dir=commands 'print' ./




lint:
	@echo "Linting Python files"
	flake8 --exclude=migrations --ignore=E501,E225,E121,E123,E124,E125,E127,E128 raven || exit 1
	@echo ""
