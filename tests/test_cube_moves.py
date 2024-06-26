
import os
import json
import unittest
from copy import deepcopy

from modules.cube import RubiksCube

ALL_POSSIBLE_MOVES = [

    ["top", "horizontal", "left"],
    ["top", "horizontal", "right"],
    ["middle", "horizontal", "left"],
    ["middle", "horizontal", "right"],
    ["bottom", "horizontal", "left"],
    ["bottom", "horizontal", "right"],
    ["left", "vertical", "up"],
    ["left", "vertical", "down"],
    ["right", "vertical", "up"],
    ["right", "vertical", "down"],
    ["middle", "vertical", "up"],
    ["middle", "vertical", "down"]

]

class TestMoves( unittest.TestCase ):

    def run_test_file( self, test_data_path ):
        """
        Tests single cube moves and validates it returns as expected
        """
        file_data = None
        if not os.path.exists( test_data_path ):
            raise Exception(f"Given file path does not exist - {test_data_path}")
        
        with open( test_data_path, "r" ) as file:
            file_data = json.load( file )
            file.close()
        TEST_MOVE = file_data.get("TEST_MOVE")
        TEST_SOLUTION = file_data.get("TEST_SOLUTION")
        TEST_CUBE_OVERRIDE = file_data.get("TEST_CUBE_OVERRIDE", None)
        if TEST_CUBE_OVERRIDE is not None:
            print(f"USING CUSTOM CUBE OVERRIDE: {TEST_CUBE_OVERRIDE}")
        
        cube_client = RubiksCube(cube=TEST_CUBE_OVERRIDE)

        if "move_cube" in test_data_path:
            section, orientation, direction, turns = TEST_MOVE
            cube_client.move_cube(
                section=section,
                orientation=orientation,
                direction=direction,
                turns=turns
            )
        elif "rotate_cube" in test_data_path:
            direction, turns = TEST_MOVE
            print( direction, turns )
            cube_client.rotate_cube( 
                direction=direction,
                turns=turns
            )
        cube_client.visualize_cube()
        for move_check in TEST_SOLUTION:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")
            err_details = f"generated_side ({test_side}): {generated_side} does not match expected value ({test_side}): {expected_value}"
            self.assertEqual(
                generated_side,
                expected_value,
                err_details
            )

    def validate_custom_moves( self, test_data_path ):
        """
        Validates list of mutations returns expected response
        """

        file_data = None
        if not os.path.exists( test_data_path ):
            raise Exception(f"Given file path does not exist - {test_data_path}")
        
        with open( test_data_path, "r" ) as file:
            file_data = json.load( file )
            file.close()

        TEST_CUBE_MOVES_INPUT = file_data.get("TEST_CUBE_MOVES_INPUT")
        TEST_SOLUTION = file_data.get("TEST_SOLUTION")

        cube_client = RubiksCube()

        for move in TEST_CUBE_MOVES_INPUT:
            action = move.get("action")

            if action == "move_cube":
                section =  move.get("section")
                orientation =  move.get("orientation")
                direction =  move.get("direction")
                turns =  move.get("turns")
                cube_client.move_cube(section, orientation, direction, turns)

            elif action == "rotate_cube":
                direction =  move.get("direction")
                turns =  move.get("turns")
                cube_client.rotate_cube( direction, turns )
            
        for move_check in TEST_SOLUTION:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")
            err_details = f"generated_side ({test_side}): {generated_side} does not match expected value ({test_side}): {expected_value}"
            self.assertEqual(
                generated_side,
                expected_value,
                err_details
            )

    def solve_cube_step( self, test_data_path ):
        file_data = None
        if not os.path.exists( test_data_path ):
            raise Exception(f"Given file path does not exist - {test_data_path}")
        
        with open( test_data_path, "r" ) as file:
            file_data = json.load( file )
            file.close()

        STEP_NAME = file_data.get("STEP_NAME")
        TEST_SOLUTION = file_data.get("TEST_SOLUTION")
        TEST_CUBE_OVERRIDE = file_data.get("TEST_CUBE_OVERRIDE", None)
        STEP_NUMBER = file_data.get( "STEP_NUMBER", None )
        STEPS_TO_SOLVE = file_data.get( "STEPS_TO_SOLVE", None )

        cube_client = RubiksCube( cube=TEST_CUBE_OVERRIDE )
        solve_steps = cube_client.solve_cube( STEP_NUMBER )

        for move_check in TEST_SOLUTION:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")

            for row in range( len( expected_value ) ):
                for sticker in range( len( expected_value[row] ) ):
                    expected_sticker = expected_value[row][sticker]
                    generated_sticker = generated_side[row][sticker]

                    if expected_sticker:
                        err_details = f"\nERROR IN SOLVE STEP: {STEP_NAME}\n - generated_side ({test_side}): \n{generated_side} \ndoes not match expected value ({test_side}): \n{expected_value}"
                        self.assertEqual(
                            expected_sticker,
                            generated_sticker,
                            err_details
                        )

        # print( solve_steps )
        if STEPS_TO_SOLVE is not None:
            self.assertEqual( solve_steps, STEPS_TO_SOLVE )

    def run_check_brick_value_test( self, test_data_path ):
        file_data = None
        if not os.path.exists( test_data_path ):
            raise Exception(f"Given file path does not exist - {test_data_path}")
        
        with open( test_data_path, "r" ) as file:
            file_data = json.load( file )
            file.close()

        FUNCTION_INPUT = file_data.get("FUNCTION_INPUT")
        TEST_SOLUTION = file_data.get("TEST_SOLUTION")
        TEST_CUBE_OVERRIDE = file_data.get("TEST_CUBE_OVERRIDE", None)

        cube_client = RubiksCube( cube = TEST_CUBE_OVERRIDE )
        side_name, row, direction = FUNCTION_INPUT
        generated_value = cube_client.check_brick_value( side_name, row, direction )

        print( f"Generated value: {generated_value}" )
        print( f"Expected value: {TEST_SOLUTION}" )

        self.assertNotEqual( generated_value, None, "generated_value should not return None" )
        self.assertEqual( len( generated_value ), len( TEST_SOLUTION ), f"length of generated_value: {len(generated_value)} should be the same as the expected: {len(TEST_SOLUTION)}"  )
        
        for test_key, test_value in TEST_SOLUTION.items():
            print( test_key, test_value )
            generated_value_item_value = generated_value.get( test_key )

            print(f"generated_value_item_value: {generated_value_item_value}")
            self.assertEqual( generated_value_item_value, test_value )
            self.assertIn( test_key, generated_value )

    def process_step_1_permutations( self, permutation_storage_filepath ):
        permutation_storage_data = []
        permutation_storage_length = len( permutation_storage_data )
        no_data_error = None

        with open( permutation_storage_filepath, "r" ) as permutation_storage:
            try:
                json_data = json.load( permutation_storage )
                permutation_storage_data = json_data
                permutation_storage_length = len( permutation_storage_data )
            except Exception as e:
                no_data_error = f"Error reading permutations file, regenerate using 'make generate-test-permutations' - error: {e}"
                print( no_data_error )

        for test_input_data in permutation_storage_data:

            ID = test_input_data.get( "ID" )
            PERMUTATION_MOVES = test_input_data.get("PERMUTATION_MOVES")

            print( f"Test: {ID}/{permutation_storage_length}" )

            cube_client = RubiksCube()

            for mutation in PERMUTATION_MOVES:

                function_name = mutation[0]

                if function_name == "move_cube":
                    _, section, orientation, direction, turns = mutation

                    if 3 >= turns >= 1:
                        cube_client.move_cube( section, orientation, direction, turns )

                elif function_name == "rotate_cube":
                    _, direction, turns = mutation
                    if 3 >= turns >= 1:
                        cube_client.rotate_cube( direction, turns )

            solve_steps = cube_client.solve_cube( step_override=1, test_id=ID )

            top_side_color = cube_client.top_side[1][1]
            front_side_color = cube_client.front_side[1][1]
            back_side_color = cube_client.back_side[1][1]
            left_side_color = cube_client.left_side[1][1]
            right_side_color = cube_client.right_side[1][1]

            test_solution = [
                {
                    "expected_side": "top_side",
                    "expected_value": [
                        [ None, top_side_color, None ],
                        [ top_side_color, top_side_color, top_side_color ],
                        [ None, top_side_color, None ]
                    ]
                },
                {
                    "expected_side": "front_side",
                    "expected_value": [
                        [ None, front_side_color, None ],
                        [ None, front_side_color, None ],
                        [ None, None, None ]
                    ]
                },
                {
                    "expected_side": "bottom_side",
                    "expected_value": [
                        [ None, None, None ],
                        [ None, None, None ],
                        [ None, None, None ]
                    ]
                },
                {
                    "expected_side": "back_side",
                    "expected_value": [
                        [ None, back_side_color, None ],
                        [ None, back_side_color, None ],
                        [ None, None, None ]
                    ]
                },
                {
                    "expected_side": "left_side",
                    "expected_value": [
                        [ None, left_side_color, None ],
                        [ None, left_side_color, None ],
                        [ None, None, None ]
                    ]
                },
                {
                    "expected_side": "right_side",
                    "expected_value": [
                        [ None, right_side_color, None ],
                        [ None, right_side_color, None ],
                        [ None, None, None ]
                    ]
                }
            ]

            for move_check in test_solution:
                test_side = move_check.get("expected_side")
                generated_side = cube_client[ test_side ]
                expected_value = move_check.get("expected_value")

                for row in range( len( expected_value ) ):
                    for sticker in range( len( expected_value[row] ) ):
                        expected_sticker = expected_value[row][sticker]
                        generated_sticker = generated_side[row][sticker]

                        if expected_sticker:
                            err_details = f'\nERROR IN SOLVE STEP FOR PERMUTATION: "ID": {ID}\n - generated_side ({test_side}): \n{generated_side} \ndoes not match expected value ({test_side}): \n{expected_value}'
                            self.assertEqual(
                                expected_sticker,
                                generated_sticker,
                                err_details
                            )

            # self.assertEqual( solve_steps, [] )
                            
        self.assertEqual( no_data_error, None )

    def process_step_1__json_permutations( self, permutation_storage_filepath ):
        permutation_storage_data = []
        permutation_storage_length = len( permutation_storage_data )
        no_data_error = None

        permutation_storage_data = []
        permutation_storage_length = len( permutation_storage_data )
        no_data_error = None

        with open( permutation_storage_filepath, "r" ) as permutation_storage:
            try:
                json_data = json.load( permutation_storage )
                permutation_storage_data = json_data
                permutation_storage_length = len( permutation_storage_data )
            except Exception as e:
                no_data_error = f"Error reading permutations file, regenerate using 'make generate-test-permutations' - error: {e}"
                print( no_data_error )

        ID = permutation_storage_data.get( "ID" )
        TEST_CUBE_OVERRIDE = permutation_storage_data.get("TEST_CUBE_OVERRIDE")

        cube_client = RubiksCube(raw_cube=TEST_CUBE_OVERRIDE)

        solve_steps = cube_client.solve_cube( step_override=1, test_id=ID )

        top_side_color = cube_client.top_side[1][1]
        front_side_color = cube_client.front_side[1][1]
        back_side_color = cube_client.back_side[1][1]
        left_side_color = cube_client.left_side[1][1]
        right_side_color = cube_client.right_side[1][1]

        test_solution = [
            {
                "expected_side": "top_side",
                "expected_value": [
                    [ None, top_side_color, None ],
                    [ top_side_color, top_side_color, top_side_color ],
                    [ None, top_side_color, None ]
                ]
            },
            {
                "expected_side": "front_side",
                "expected_value": [
                    [ None, front_side_color, None ],
                    [ None, front_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "bottom_side",
                "expected_value": [
                    [ None, None, None ],
                    [ None, None, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "back_side",
                "expected_value": [
                    [ None, back_side_color, None ],
                    [ None, back_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "left_side",
                "expected_value": [
                    [ None, left_side_color, None ],
                    [ None, left_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "right_side",
                "expected_value": [
                    [ None, right_side_color, None ],
                    [ None, right_side_color, None ],
                    [ None, None, None ]
                ]
            }
        ]

        for move_check in test_solution:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")

            for row in range( len( expected_value ) ):
                for sticker in range( len( expected_value[row] ) ):
                    expected_sticker = expected_value[row][sticker]
                    generated_sticker = generated_side[row][sticker]

                    if expected_sticker:
                        err_details = f'\nERROR IN SOLVE STEP FOR PERMUTATION: "ID": {ID}\n - generated_side ({test_side}): \n{generated_side} \ndoes not match expected value ({test_side}): \n{expected_value}'
                        self.assertEqual(
                            expected_sticker,
                            generated_sticker,
                            err_details
                        )
        self.assertEqual( no_data_error, None )

    def step_1_random_shuffle( self, shuffle_times=0 ):
        cube_client = RubiksCube()
        cube_client.shuffle_cube( shuffle_times )
        cube_client.solve_cube( step_override=1 )

        top_side_color = cube_client.top_side[1][1]
        front_side_color = cube_client.front_side[1][1]
        back_side_color = cube_client.back_side[1][1]
        left_side_color = cube_client.left_side[1][1]
        right_side_color = cube_client.right_side[1][1]

        test_solution = [
            {
                "expected_side": "top_side",
                "expected_value": [
                    [ None, top_side_color, None ],
                    [ top_side_color, top_side_color, top_side_color ],
                    [ None, top_side_color, None ]
                ]
            },
            {
                "expected_side": "front_side",
                "expected_value": [
                    [ None, front_side_color, None ],
                    [ None, front_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "bottom_side",
                "expected_value": [
                    [ None, None, None ],
                    [ None, None, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "back_side",
                "expected_value": [
                    [ None, back_side_color, None ],
                    [ None, back_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "left_side",
                "expected_value": [
                    [ None, left_side_color, None ],
                    [ None, left_side_color, None ],
                    [ None, None, None ]
                ]
            },
            {
                "expected_side": "right_side",
                "expected_value": [
                    [ None, right_side_color, None ],
                    [ None, right_side_color, None ],
                    [ None, None, None ]
                ]
            }
        ]

    def random_shuffle_and_solve( self, shuffle_times=0 ):
        cube_client = RubiksCube()
        cube_client.shuffle_cube( shuffle_times )
        cube_client.solve_cube()

        top_side_color = cube_client.top_side[1][1]
        front_side_color = cube_client.front_side[1][1]
        back_side_color = cube_client.back_side[1][1]
        left_side_color = cube_client.left_side[1][1]
        right_side_color = cube_client.right_side[1][1]
        bottom_side_color = cube_client.bottom_side[1][1]

        test_solution = [
            {
                "expected_side": "top_side",
                "expected_value": [
                    [ top_side_color, top_side_color, top_side_color ],
                    [ top_side_color, top_side_color, top_side_color ],
                    [ top_side_color, top_side_color, top_side_color ]
                ]
            },
            {
                "expected_side": "front_side",
                "expected_value": [
                    [ front_side_color, front_side_color, front_side_color ],
                    [ front_side_color, front_side_color, front_side_color ],
                    [ front_side_color, front_side_color, front_side_color ]
                ]
            },
            {
                "expected_side": "bottom_side",
                "expected_value": [
                    [ bottom_side_color, bottom_side_color, bottom_side_color ],
                    [ bottom_side_color, bottom_side_color, bottom_side_color ],
                    [ bottom_side_color, bottom_side_color, bottom_side_color ]
                ]
            },
            {
                "expected_side": "back_side",
                "expected_value": [
                    [ back_side_color, back_side_color, back_side_color ],
                    [ back_side_color, back_side_color, back_side_color ],
                    [ back_side_color, back_side_color, back_side_color ]
                ]
            },
            {
                "expected_side": "left_side",
                "expected_value": [
                    [ left_side_color, left_side_color, left_side_color ],
                    [ left_side_color, left_side_color, left_side_color ],
                    [ left_side_color, left_side_color, left_side_color ]
                ]
            },
            {
                "expected_side": "right_side",
                "expected_value": [
                    [ right_side_color, right_side_color, right_side_color ],
                    [ right_side_color, right_side_color, right_side_color ],
                    [ right_side_color, right_side_color, right_side_color ]
                ]
            }
        ]

        for move_check in test_solution:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")

            for row in range( len( expected_value ) ):
                for sticker in range( len( expected_value[row] ) ):
                    expected_sticker = expected_value[row][sticker]
                    generated_sticker = generated_side[row][sticker]

                    if expected_sticker:
                        err_details = f'\nERROR IN STEP COMPLETE RANDOM SHUFFLE:\n - generated_side ({test_side}): \n{generated_side} \ndoes not match expected value ({test_side}): \n{expected_value}'
                        self.assertEqual(
                            expected_sticker,
                            generated_sticker,
                            err_details
                        )

        for move_check in test_solution:
            test_side = move_check.get("expected_side")
            generated_side = cube_client[ test_side ]
            expected_value = move_check.get("expected_value")

            for row in range( len( expected_value ) ):
                for sticker in range( len( expected_value[row] ) ):
                    expected_sticker = expected_value[row][sticker]
                    generated_sticker = generated_side[row][sticker]

                    if expected_sticker:
                        err_details = f'\nERROR IN STEP 1 RANDOM SHUFFLE:\n - generated_side ({test_side}): \n{generated_side} \ndoes not match expected value ({test_side}): \n{expected_value}'
                        self.assertEqual(
                            expected_sticker,
                            generated_sticker,
                            err_details
                        )

    # ------- TEST EVERY POSSIBLE 1 MOVE ( function: move_cube ) -------
    # Format: test__class_function__section_orientation_direction_turns

    def test__move_cube__top_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__top_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_down_1.json" 
        self.run_test_file( test_data_path )


    # ------- TEST EVERY POSSIBLE 2 MOVES ( function: move_cube ) -------
            
    def test__move_cube__top_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__top_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_down_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_down_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_down_2.json" 
        self.run_test_file( test_data_path )


    # ------- TEST EVERY POSSIBLE 3 MOVES ( function: move_cube ) -------
            
    def test__move_cube__top_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__top_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    # ------- TEST EVERY POSSIBLE 4 MOVES ( function: move_cube ) -------

    def test__move_cube__top_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__top_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__top_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__bottom_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__left_vertical_down_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__right_vertical_down_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/move_cube__middle_vertical_down_4.json" 
        self.run_test_file( test_data_path )



    # ------- CUSTOM CUBE 1 MOVE INPUT TESTS ( function: move_cube ) -------
        
    def test__custom__move_cube__left_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM CUBE 2 MOVE INPUT TESTS ( function: move_cube ) -------
        
    def test__custom__move_cube__left_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_down_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_down_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_left_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_left_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_right_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_right_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_up_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_up_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_down_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_down_2.json" 
        self.run_test_file( test_data_path )


    # ------- CUSTOM CUBE 3 MOVE INPUT TESTS ( function: move_cube ) -------
        
    def test__custom__move_cube__left_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_left_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_left_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_right_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_right_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_up_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_up_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_down_3( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_down_3.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM CUBE 4 MOVE INPUT TESTS ( function: move_cube ) -------
        
    def test__custom__move_cube__left_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_down_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__left_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__right_vertical_down_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__top_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__bottom_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_left_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_left_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_horizontal_right_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_horizontal_right_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_up_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_up_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__middle_vertical_down_4( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__middle_vertical_down_4.json" 
        self.run_test_file( test_data_path )

    # ------- TEST EVERY POSSIBLE MOVE ( function: rotate_cube ) -------
        
    def test__rotate_cube__left_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__left_1.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__left_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__left_2.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__left_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__left_3.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__left_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__left_4.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__right_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__right_1.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__right_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__right_2.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__right_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__right_3.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__right_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__right_4.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__up_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__up_1.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__up_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__up_2.json" 
        self.run_test_file( test_data_path )
        
    def test__rotate_cube__up_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__up_3.json" 
        self.run_test_file( test_data_path )
        
    def test__rotate_cube__up_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__up_4.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__down_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__down_1.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__down_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__down_2.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__down_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__down_3.json" 
        self.run_test_file( test_data_path )

    def test__rotate_cube__down_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/rotate_cube__down_4.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM CUBE INPUT TESTS ( function: rotate_cube ) -------
        
    def test__custom__rotate_cube_left_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_4.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_4.json" 
        self.run_test_file( test_data_path )
        
    def test__custom__rotate_cube_down_1( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_down_2( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_2.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_down_3( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_3.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_down_4( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_4.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM COMPLICATED CUBE INPUT TESTS ( function: rotate_cube ) -------
        
    def test__custom__rotate_cube_down_1_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_1_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_down_2_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_2_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_down_3_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_3_complicated.json" 
        self.run_test_file( test_data_path )
        
    def test__custom__rotate_cube_down_4_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__down_4_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_1_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_1_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_2_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_2_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_3_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_3_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_up_4_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__up_4_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_1_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_1_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_2_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_2_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_3_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_3_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_left_4_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__left_4_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_1_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_1_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_2_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_2_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_3_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_3_complicated.json" 
        self.run_test_file( test_data_path )

    def test__custom__rotate_cube_right_4_complicated( self ):
        test_data_path = "tests/test_cases/rotate_cube/custom__rotate_cube__right_4_complicated.json" 
        self.run_test_file( test_data_path )

    # SIMPLE SOLVE
        
    def test__custom__simple_solve_1( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__simple_solve_1.json" 
        self.run_test_file( test_data_path ) 

    def test__custom__simple_solve_2( self ):
        test_data_path = "tests/test_cases/move_cube/custom__move_cube__simple_solve_2.json" 
        self.run_test_file( test_data_path ) 


    # ------- TEST RANDOM SHUFFLE -------
    
    def test__custom__random_shuffle_10_moves( self ):
        test_data_path = "tests/test_cases/move_test/move_10_times.json"
        self.validate_custom_moves( test_data_path  )

    def test__custom__validate_test_solve_cube( self ):
        test_data_path = "tests/test_cases/move_test/validate_test_solve_cube.json"
        self.validate_custom_moves( test_data_path )

    # ------- TESTING SOLVE STEP 1 TOP CROSS -------

    def test__step_1__do_nothing( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__do_nothing.json"
        self.solve_cube_step( test_data_path )

    def test__step_1__do_nothing__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__in_place__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE LEFT PIECE --- TOP ROW

    def test__top_cross__1_0__top__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__back.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__front.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__top__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__top__front__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE LEFT PIECE --- MIDDLE ROW

    def test__top_cross__1_0__middle__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__back_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__back_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__front_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__front_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__left_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__left_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__left_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__left_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__right_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__right_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__middle__right_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__middle__right_right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE LEFT PIECE --- BOTTOM ROW
        
    def test__top_cross__1_0__bottom__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__bottom__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__back.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_0__bottom__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__front__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__bottom__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__front.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_0__bottom__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__bottom__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__left.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_0__bottom__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_0__bottom__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_0__bottom__right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE BOTTOM MIDDLE --- TOP ROW

    def test__top_cross__2_1__top__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__back.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__front.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__top__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__top__front__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE BOTTOM MIDDLE --- MIDDLE ROW

    def test__top_cross__2_1__middle__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__back_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__back_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__front_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__front_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__left_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__left_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__left_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__left_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__right_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__right_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__middle__right_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__middle__right_right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE BOTTOM MIDDLE PIECE --- BOTTOM ROW
        
    def test__top_cross__2_1__bottom__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__bottom__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__back.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__2_1__bottom__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__front__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__bottom__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__front.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__2_1__bottom__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__bottom__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__left.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__2_1__bottom__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__2_1__bottom__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__2_1__bottom__right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE TOP MIDDLE --- TOP ROW

    def test__top_cross__0_1__top__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__back.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__front.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__top__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__top__front__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE TOP MIDDLE --- MIDDLE ROW

    def test__top_cross__0_1__middle__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__back_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__back_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__front_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__front_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__left_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__left_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__left_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__left_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__right_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__right_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__middle__right_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__middle__right_right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE TOP MIDDLE PIECE --- BOTTOM ROW
        
    def test__top_cross__0_1__bottom__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__bottom__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__back.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__0_1__bottom__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__front__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__bottom__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__front.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__0_1__bottom__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__bottom__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__left.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__0_1__bottom__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__0_1__bottom__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__0_1__bottom__right.json"
        self.solve_cube_step( test_data_path )
    
    # ------- TOP SIDE MIDDLE RIGHT --- TOP ROW

    def test__top_cross__1_2__top__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__back.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__front.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__top__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__top__front__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE MIDDLE RIGHT --- MIDDLE ROW

    def test__top_cross__1_2__middle__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__back_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__back_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__front_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__front_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__left_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__left_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__left_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__left_right.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__right_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__right_left.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__middle__right_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__middle__right_right.json"
        self.solve_cube_step( test_data_path )

    # ------- TOP SIDE MIDDLE RIGHT PIECE --- BOTTOM ROW
        
    def test__top_cross__1_2__bottom__back__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__back__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__bottom__back( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__back.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_2__bottom__front__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__front__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__bottom__front( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__front.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_2__bottom__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__bottom__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__left.json"
        self.solve_cube_step( test_data_path )
        
    def test__top_cross__1_2__bottom__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__top_cross__1_2__bottom__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_1/test__top_cross__1_2__bottom__right.json"
        self.solve_cube_step( test_data_path )


    # ------- STEP 2 TESTS -------
    
    # ------- STEP 2 - FRONT LEFT PIECE -------
    def test__step_2__front_left__top__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__top__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/top__2__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_left__bottom__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_left/bottom__2__2__240.json"
        self.solve_cube_step( test_data_path )

    # ------- STEP 2 - FRONT RIGHT PIECE -------
    def test__step_2__front_right__top__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__top__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/top__2__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__front_right__bottom__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/front_right/bottom__2__2__240.json"
        self.solve_cube_step( test_data_path )

    # # ------- STEP 2 - BACK LEFT PIECE -------
    def test__step_2__back_left__top__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__top__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/top__2__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_left__bottom__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_left/bottom__2__2__240.json"
        self.solve_cube_step( test_data_path )

    # ------- STEP 2 - BACK RIGHT PIECE -------
    def test__step_2__back_right__top__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__top__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/top__2__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__0__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__0__2__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__0__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__0__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__0__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__0__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__0__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__0__240.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__2__0( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__2__0.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__2__120( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__2__120.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__back_right__bottom__2__2__240( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/back_right/bottom__2__2__240.json"
        self.solve_cube_step( test_data_path )

    # RANDOM STEP 2 FULL TESTS
    def test__step_2__full_test_1( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/test_cases/test_1.json"
        self.solve_cube_step( test_data_path )

    def test__step_2__full_test_2( self ):
        test_data_path = "tests/test_cases/solve_cube/step_2/test_cases/test_2.json"
        self.solve_cube_step( test_data_path )


    # ------- STEP 3 TESTS -------
    # Flip cube tests already in place

    # ------- STEP 4 TESTS -------

    # ------- BACK LEFT -------
        
    def test__step_4__back_left__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/back_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__back_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/back_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/back_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__back_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/back_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/front_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__front_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/front_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/front_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__front_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/front_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__bottom_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__bottom_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__bottom_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__bottom_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__top_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__top_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_left__top_side__top_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_left/top_side__top_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- BACK RIGHT -------
        
    def test__step_4__back_right__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/back_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__back_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/back_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/back_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__back_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/back_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/front_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__front_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/front_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/front_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__front_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/front_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__bottom_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__bottom_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__bottom_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__bottom_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__top_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__top_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__back_right__top_side__top_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/back_right/top_side__top_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- FRONT LEFT -------
        
    def test__step_4__front_left__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/back_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__back_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/back_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/back_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__back_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/back_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/front_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__front_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/front_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/front_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__front_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/front_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__bottom_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__bottom_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__bottom_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__bottom_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__top_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__top_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_left__top_side__top_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_left/top_side__top_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- FRONT RIGHT -------
        
    def test__step_4__front_right__back_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/back_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__back_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/back_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__back_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/back_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__back_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/back_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__front_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/front_left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__front_left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/front_left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__front_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/front_right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__front_right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/front_right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__bottom_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__bottom_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__bottom_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__bottom_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__left.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__left__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__left__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__right.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__right__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__right__reversed.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__top_middle( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__top_middle.json"
        self.solve_cube_step( test_data_path )

    def test__step_4__front_right__top_side__top_middle__reversed( self ):
        test_data_path = "tests/test_cases/solve_cube/step_4/front_right/top_side__top_middle__reversed.json"
        self.solve_cube_step( test_data_path )

    # ------- STEP 5 TESTS -------

    # L tests
    def test_step_5__L__top_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/L_tests/top_left.json"
        self.solve_cube_step( test_data_path )

    def test_step_5__L__top_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/L_tests/top_right.json"
        self.solve_cube_step( test_data_path )

    def test_step_5__L__bottom_left( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/L_tests/bottom_left.json"
        self.solve_cube_step( test_data_path )

    def test_step_5__L__bottom_right( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/L_tests/bottom_right.json"
        self.solve_cube_step( test_data_path )

    # I tests
    def test_step_5__I__horizontal( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/I_tests/horizontal.json"
        self.solve_cube_step( test_data_path )

    def test_step_5__I__vertical( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/I_tests/vertical.json"
        self.solve_cube_step( test_data_path )

    # No Cross tests
    def test_step_5__I__no_cross( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/no_cross.json"
        self.solve_cube_step( test_data_path )

    # RANDOM TESTS FROM RUN CUBE
    def test_step_5__random_test_1( self ):
        test_data_path = "tests/test_cases/solve_cube/step_5/random_tests/1.json"
        self.solve_cube_step( test_data_path )


    # ------- STEP 6 TESTS -------

    def test_step_6__random_test__1( self ):
        test_data_path = "tests/test_cases/solve_cube/step_6/random_tests/1.json"
        self.solve_cube_step( test_data_path )

    def test_step_6__random_test__2( self ):
        test_data_path = "tests/test_cases/solve_cube/step_6/random_tests/2.json"
        self.solve_cube_step( test_data_path )

    def test_step_6__random_test__3( self ):
        test_data_path = "tests/test_cases/solve_cube/step_6/random_tests/3.json"
        self.solve_cube_step( test_data_path )

    def test_step_6__random_test__4( self ):
        test_data_path = "tests/test_cases/solve_cube/step_6/random_tests/4.json"
        self.solve_cube_step( test_data_path )

    def test_step_6__random_test__5( self ):
        test_data_path = "tests/test_cases/solve_cube/step_6/random_tests/5.json"
        self.solve_cube_step( test_data_path )


    # ------- STEP 8 TESTS -------

    def test_step_8__random_test__1( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/1.json"
        self.solve_cube_step( test_data_path )

    def test_step_8__random_test__2( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/2.json"
        self.solve_cube_step( test_data_path )

    def test_step_8__random_test__3( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/3.json"
        self.solve_cube_step( test_data_path )

    def test_step_8__random_test__4( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/4.json"
        self.solve_cube_step( test_data_path )

    def test_step_8__random_test__5( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/5.json"
        self.solve_cube_step( test_data_path )

    def test_step_8__random_test__6( self ):
        test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/6.json"
        self.solve_cube_step( test_data_path )

    # randomly rotating the cube supplied an invalid block, fixing this to only rotate or move, to not mess up the cube state when doing both
    # def test_step_8__random_test__7( self ):
    #     test_data_path = "tests/test_cases/solve_cube/step_8/random_tests/7.json"
    #     self.solve_cube_step( test_data_path )
    


        
    # ------- BATCH TESTS -------

    # def test__step_1_permutations__batch_1( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_1.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_2( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_2.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_3( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_3.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_4( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_4.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_5( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_5.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_6( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_6.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_7( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_7.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_8( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_8.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_9( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_9.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_10( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_10.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

    # def test__step_1_permutations__batch_11( self ):
    #     permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/batches/batch_11.json"
    #     self.process_step_1_permutations( permutation_storage_filepath )

  
        
    # === RANDOM TESTS ===
        
    def test__step_1__random_shuffle_1( self ):
        self.step_1_random_shuffle( 1 )

    def test__step_1__random_shuffle_2( self ):
        self.step_1_random_shuffle( 2 )

    def test__step_1__random_shuffle_3( self ):
        self.step_1_random_shuffle( 3 )

    def test__step_1__random_shuffle_4( self ):
        self.step_1_random_shuffle( 4 )

    def test__step_1__random_shuffle_5( self ):
        self.step_1_random_shuffle( 5 )

    def test__step_1__random_shuffle_10( self ):
        self.step_1_random_shuffle( 10 )

    def test__step_1__random_shuffle_15( self ):
        self.step_1_random_shuffle( 15 )

    def test__step_1__random_shuffle_20( self ):
        self.step_1_random_shuffle( 20 )

    def test__step_1__random_shuffle_20x2( self ):
        self.step_1_random_shuffle( 20 )

    def test__step_1__random_shuffle_20x3( self ):
        self.step_1_random_shuffle( 20 )

    def test__step_1__random_shuffle_20x4( self ):
        self.step_1_random_shuffle( 20 )

    def test__step_1__random_shuffle_20x5( self ):
        self.step_1_random_shuffle( 20 )

    def test__step_1__random_shuffle_30( self ):
        self.step_1_random_shuffle( 30 )

    def test__step_1__random_shuffle_40( self ):
        self.step_1_random_shuffle( 40 )

    def test__step_1__random_shuffle_50( self ):
        self.step_1_random_shuffle( 50 )

    def test__step_1__random_shuffle_100_1( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_2( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_3( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_4( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_5( self ):
        self.random_shuffle_and_solve( 100 )
        
    def test__step_1__random_shuffle_100_6( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_7( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_8( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_100_9( self ):
        self.random_shuffle_and_solve( 100 )
        
    def test__step_1__random_shuffle_100_10( self ):
        self.random_shuffle_and_solve( 100 )

    def test__step_1__random_shuffle_1000_1( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_2( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_3( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_4( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_5( self ):
        self.random_shuffle_and_solve( 1000 )
        
    def test__step_1__random_shuffle_1000_6( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_7( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_8( self ):
        self.random_shuffle_and_solve( 1000 )

    def test__step_1__random_shuffle_1000_9( self ):
        self.random_shuffle_and_solve( 1000 )
        
    def test__step_1__random_shuffle_1000_10( self ):
        self.random_shuffle_and_solve( 1000 )

if __name__ == '__main__':
    unittest.main()