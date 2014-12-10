# Shell to use with Make
SHELL := /bin/sh

# Set important Paths
PROJECT := brisera
LOCALPATH := $(CURDIR)/$(PROJECT)
PYTHONPATH := $(LOCALPATH)/
PYTHON_BIN := $(VIRTUAL_ENV)/bin

# Export targets not associated with files
.PHONY: test bootstrap pip virtualenv clean virtual_env_set install

# Clean build files
clean:
	find . -name "*.pyc" -print0 | xargs -0 rm -rf
	-rm -rf htmlcov
	-rm -rf .coverage
	-rm -rf build
	-rm -rf dist
	-rm -rf $(PROJECT).egg-info

# Targets for testing
test:
	$(PYTHON_BIN)/nosetests -v --cover-package=$(PROJECT) tests

# Targets for installation
install:
	$(PYTHON_BIN)/python setup.py install
