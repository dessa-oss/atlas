
.PHONY: devenv-start
devenv-start: devenv-stop
	cd devenv && ./configure.sh && ./start_devenv.sh

.PHONY: devenv-stop
devenv-stop:
	cd devenv && ./stop_devenv.sh

.PHONY: tests
tests: unit-tests integration-tests acceptance-tests 

.PHONY: unit-tests
unit-tests:
	./run_unit_tests.sh

.PHONY: integration-tests
integration-tests:
	./run_integration_tests.sh

.PHONY: acceptance-tests
acceptance-tests:
	./run_acceptance_tests.sh