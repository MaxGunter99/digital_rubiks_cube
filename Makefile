# THIS IS THE MAKEFILE, some useful saved commands

define COMMAND_LIST

	make activate-virtual-environment
	make run-cube
	make test-cube
	make test-cube-with-output
	make update-requirements

endef

activate-virtual-environment:
	poetry shell

run-cube:
	python3 run_me.py

test-cube:
	python -m unittest discover -v -s tests -p 'test_*.py' -b

test-cube-with-output:
	python -m unittest discover -v -s tests -p 'test_*.py' -b > tests/test_cube_moves_output.txt

update-requirements:
	poetry export -f requirements.txt --output requirements.txt
