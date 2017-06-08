.DEFAULT_GOAL := help
SHELL := /bin/bash

help:                ## Show available options with this Makefile
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.PHONY: install_doc_deps
install_doc_deps:    ## Install sphinx dependencies
install_doc_deps:
	@pip install sphinx sphinx_rtd_theme

.PHONY: docs
docs:                ## Generate all the docs
docs:    install_doc_deps
	@cd docs && sphinx-apidoc -f -o source/ ../pylogging && make html
	@echo "docs are generated in docs/build/html/index.html"
	@xdg-open docs/build/html/index.html
