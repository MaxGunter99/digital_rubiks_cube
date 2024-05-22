# THIS IS THE MAKEFILE, some useful saved commands

define COMMAND_LIST

	make activate-virtual-environment
	make run-cube
	make time-solve-average
	make test-cube
	make test-cube-with-output
	make update-requirements
	make generate-test-permutations

endef

activate-virtual-environment:
	poetry shell

run-cube:
	time python3 run_me.py

time-solve-average:
	time python3 run_average_time.py

test-cube:
	python -m unittest discover -v -s tests -p 'test_*.py' -b -f

test-cube-with-output:
	python -m unittest discover -v -s tests -p 'test_*.py' -b > tests/test_cube_moves_output.txt 2>&1

update-requirements:
	poetry export -f requirements.txt --output requirements.txt

generate-test-permutations:
	python3 generate_permutations_list.py
