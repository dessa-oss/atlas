
.PHONY: devenv-start
devenv-start: devenv-stop
	cd devenv && ./start_devenv.sh

.PHONY: devenv-stop
devenv-stop:
	cd devenv && ./stop_devenv.sh

.PHONY: devenv-configure
devenv-configure:
	cd devenv && ./configure.sh