.PHONY: install uninstall build pypi
install:
	python setup.py install

uninstall:
	pip uninstall gopher-render

build:
	pip install wheel
	python setup.py sdist bdist_wheel

pypi:
	pip install twine wheel
	python setup.py sdist bdist_wheel
	twine upload dist/*

pypi-test:
	pip install twine wheel
	python setup.py sdist bdist_wheel
	twine upload --repository testpypi dist/*

clean:
	rm dist/*
