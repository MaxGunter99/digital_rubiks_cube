
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
        solve_steps = cube_client.solve_cube()

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

        print( solve_steps )
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

    # ------- TESTING SOLVE STEPS -------

    def test__solve_cube__step_1__top_cross__p1( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p1.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p2( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p2.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p3( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p3.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p4( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p4.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p5( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p5.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p6( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p6.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p7( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p7.json"
        self.solve_cube_step( test_data_path )

    def test__solve_cube__step_1__top_cross__p8( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p8.json"
        self.solve_cube_step( test_data_path )
        
    def test__solve_cube__step_1__top_cross__p9( self ):
        test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p9.json"
        self.solve_cube_step( test_data_path )
        
    # def test__solve_cube__step_1__top_cross__p10( self ):
    #     test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p10.json"
    #     self.solve_cube_step( test_data_path )
        
    # def test__solve_cube__step_1__top_cross__p11( self ):
    #     test_data_path = "tests/test_cases/solve_cube/solve_cube__step_1__p11.json"
    #     self.solve_cube_step( test_data_path )

    def test__all_permutations( self ):
        permutation_storage_filepath = "tests/test_cases/solve_cube/all_permutations/all_cube_movement_permutations.json"
        permutation_storage_data = []
        no_data_error = None

        with open( permutation_storage_filepath, "r" ) as permutation_storage:
            try:
                json_data = json.load( permutation_storage )
                permutation_storage_data = json_data
            except Exception as e:
                no_data_error = f"Error reading permutations file, regenerate using 'make generate-test-permutations' - error: {e}"
                print( no_data_error )

        for test_input_data in permutation_storage_data:

            ID = test_input_data.get( "ID" )
            PERMUTATION_MOVES = test_input_data.get("PERMUTATION_MOVES")

            print( ID )

            # if int( ID ) >= 5000:
            #     return

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

            solve_steps = cube_client.solve_cube( step_override=1 )

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


if __name__ == '__main__':
    unittest.main()