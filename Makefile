
docs: README.md docs_src
	sphinx-apidoc -f -o ./docs_src yahoo_auction
	sphinx-build docs_src docs


test: \
	unittest \
	mypy


unittest:
	python -m unittest tests


mypy:
	mypy yahoo_auction