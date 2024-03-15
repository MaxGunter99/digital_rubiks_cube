
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

        cube_client = RubiksCube( cube=TEST_CUBE_OVERRIDE )
        cube_client.solve_cube( step_override=STEP_NUMBER )

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

        self.assertNotEqual( generated_value, None, "generated_value should not return None" )
        self.assertEqual( len( generated_value ), len( TEST_SOLUTION ), f"length of generated_value: {len(generated_value)} should be the same as the expected: {len(TEST_SOLUTION)}"  )
        self.assertEqual( generated_value, TEST_SOLUTION )

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

    # ------- TESTING CLASS FUNCTIONS -------

    # TOP SIDE
    def test__check_brick_value__top_side__bottom__center( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__bottom__center.json"
        self.run_check_brick_value_test( test_data_path )

    def test__check_brick_value__top_side__bottom__left( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__bottom__left.json"
        self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__top_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    def test__check_brick_value__top_side__middle__center( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__middle__center.json"
        self.run_check_brick_value_test( test_data_path )

    def test__check_brick_value__top_side__middle__left( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__middle__left.json"
        self.run_check_brick_value_test( test_data_path )

    def test__check_brick_value__top_side__middle__right( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__middle__right.json"
        self.run_check_brick_value_test( test_data_path )

    def test__check_brick_value__top_side__top__center( self ):
        test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__top__center.json"
        self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__top_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__top_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__top_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

        

    # FRONT SIDE
    # def test__check_brick_value__front_side__bottom__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__bottom__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__front_side__bottom__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__bottom__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__front_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__front_side__middle__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__middle__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__front_side__middle__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__middle__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__front_side__middle__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__middle__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__front_side__top__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__top__center.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__front_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__front_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__front_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # BOTTOM SIDE
    # def test__check_brick_value__bottom_side__bottom__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__bottom__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__bottom_side__bottom__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__bottom__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__bottom_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__bottom_side__middle__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__middle__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__bottom_side__middle__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__middle__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__bottom_side__middle__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__middle__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__bottom_side__top__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__top__center.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__bottom_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__bottom_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__bottom_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # BACK SIDE
    # def test__check_brick_value__back_side__bottom__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__bottom__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__back_side__bottom__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__bottom__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__back_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__back_side__middle__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__middle__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__back_side__middle__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__middle__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__back_side__middle__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__middle__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__back_side__top__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__top__center.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__back_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__back_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__back_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # LEFT SIDE
    # def test__check_brick_value__left_side__bottom__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__bottom__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__left_side__bottom__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__bottom__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__left_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__left_side__middle__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__middle__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__left_side__middle__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__middle__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__left_side__middle__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__middle__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__left_side__top__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__top__center.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__left_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__left_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__left_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # RIGHT SIDE
    # def test__check_brick_value__right_side__bottom__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__bottom__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__right_side__bottom__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__bottom__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__right_side__bottom__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__bottom__right.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__right_side__middle__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__middle__center.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__right_side__middle__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__middle__left.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__right_side__middle__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__middle__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # def test__check_brick_value__right_side__top__center( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__top__center.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__right_side__top__left( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__top__left.json"
    #     self.run_check_brick_value_test( test_data_path )
        
    # def test__check_brick_value__right_side__top__right( self ):
    #     test_data_path = "tests/test_cases/class_function_tests/check_brick_value__right_side__top__right.json"
    #     self.run_check_brick_value_test( test_data_path )

    # ------- TESTING SOLVE STEPS -------
        
    # def test__solve_cube__step_1( self ):
    #     test_data_path = "tests/test_cases/move_test/solve_step_1.json"
    #     self.solve_cube_step( test_data_path )


if __name__ == '__main__':
    unittest.main()