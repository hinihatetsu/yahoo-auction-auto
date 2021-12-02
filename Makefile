
docs: README.md docs_src
	sphinx-apidoc -f -o ./docs_src yahoo_auction_auto
	sphinx-build docs_src docs


test: mypy unittest


unittest:
	python -m unittest tests


mypy:
	mypy yahoo_auction_auto tests