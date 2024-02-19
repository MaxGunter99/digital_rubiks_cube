
# THIS IS THE MAKEFILE, some useful saved commands

define COMMAND_LIST

	make run-cube
	make test-cube

endef

activate-virtual-environment:
	potry shell

run-cube:
	python3 run_me.py

test-cube:
	python -m unittest discover -v -s tests -p 'test_*.py'