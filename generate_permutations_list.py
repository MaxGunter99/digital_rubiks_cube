
import json
from itertools import permutations, product

permutation_storage_filepath = "tests/test_cases/solve_cube/all_cube_movement_permutations.json"
move_cube_horizontal_options = [
    ["move_cube"],
    ["top", "middle", "bottom"],
    ["horizontal"],
    ["left", "right"],
    [ 0, 1, 2, 3, 4 ]
]
move_cube_vertical_options = [
    ["move_cube"],
    ["left", "right"],
    ["vertical"],
    ["up", "down"],
    [ 0, 1, 2, 3, 4 ]
]
rotate_cube_options = [
    ["rotate_cube"],
    ["left", "right", "up", "down"],
    [ 0, 1, 2, 3, 4 ]
]

all_horizontal_permutations = list( product(*move_cube_horizontal_options) )
all_vertical_permutations = list( product(*move_cube_vertical_options) )
all_rotation_permutations = list( product(*rotate_cube_options) )

all_possible_function_inputs = all_horizontal_permutations + all_vertical_permutations + all_rotation_permutations

# input_permutations = list( permutations( all_possible_function_inputs ) )

input_permutations = []
permutation_index = 1
for move_cube_horizontal_option in all_horizontal_permutations:
    for rotate_cube_option_1 in all_rotation_permutations:
        for move_cube_vertical_option in all_vertical_permutations:
            for rotate_cube_option_2 in all_rotation_permutations:
    
                full_permutation = [ 
                    move_cube_horizontal_option, 
                    rotate_cube_option_1, 
                    move_cube_vertical_option, 
                    rotate_cube_option_2 
                ]


                test_content = {
                    "ID": permutation_index,
                    "PERMUTATION_MOVES": full_permutation
                }
                input_permutations.append( test_content )
                permutation_index += 1

with open(permutation_storage_filepath, "w") as permutation_file:
    json.dump(input_permutations, permutation_file)