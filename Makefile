
# Begin Help snippet
# Source: https://gist.github.com/prwhite/8168133#gistcomment-1727513
#COLORS
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

# Add the following 'help' target to your Makefile
# And add help text after each target name starting with '\#\#'
# A category can be added with @category
HELP_FUN = \
    %help; \
    while(<>) { push @{$$help{$$2 // 'options'}}, [$$1, $$3] if /^([a-zA-Z\-]+)\s*:.*\#\#(?:@([a-zA-Z\-]+))?\s(.*)$$/ }; \
    print "usage: make [target]\n\n"; \
    for (sort keys %help) { \
    print "${WHITE}$$_:${RESET}\n"; \
    for (@{$$help{$$_}}) { \
    $$sep = " " x (32 - length $$_->[0]); \
    print "  ${YELLOW}$$_->[0]${RESET}$$sep${GREEN}$$_->[1]${RESET}\n"; \
    }; \
    print "\n"; }
# End Help snippet

.PHONY: test reqs run help clean clean-build clean-pyc clean-test docker docker-test


help: ##@general Show this help.
	@perl -e '$(HELP_FUN)' $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ##@build remove all build, test, coverage and Python artifacts

clean-build: ##@build remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ##@build remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ##@build remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

reqs: ##@build install all python requirements
	pip install -U -r requirements.txt
	pip install -U -r tests/requirements.txt
	pip install -U pylint pytest-cov coverage coveralls codacy-coverage

test: ##@build perform tests
	py.test --cov=app tests

docker: ##@build Builds docker image
	docker build . -t payments_test

docker-test: ##@build Runs docker tests
	docker run -it --rm payments_test tests

run: ##@dev Runs development app within docker
	docker run -p 5000:500 -it --rm payments_test
