
import os
import json
import unittest
from copy import deepcopy

from modules.cube import RubiksCube


RAW_CUBE = [

    #       Left                Top                 Right
    [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],

    # Rotate Cube AWAY

    #       Left               Front                 Right
    [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],  

    # Rotate Cube AWAY

    #       Left               Bottom                Right
    [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],   

    # Rotate Cube AWAY

    #       Left                Back                 Right
    [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],
    [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],     
]

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

    # def test__move_is_implemented( self ):
    #     """
    #     Confirms valid move permutations do not raise exceptions
    #     """

    #     move_errors = []

    #     cube_client = RubiksCube()
    #     for move in ALL_POSSIBLE_MOVES:

    #         try:
    #             section, orientation, direction = move
    #             cube_client.move_cube(
    #                 section=section,
    #                 orientation=orientation,
    #                 direction=direction,
    #                 turns=1
    #             )

    #         except Exception as e:
    #             move_errors.append( e )

    #     err_details = f"Moves which raised exceptions: {move_errors}"
    #     self.assertEqual( len( move_errors ) , 0 , err_details )

    def run_test_file( self, test_data_path ):
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

    # ------- TEST EVERY POSSIBLE MOVE ( function: move_cube ) -------
    # Format: test__class_function__section_orientation_direction_turns

    def test__move_cube__top_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube__top_horizontal_left_1.json" 
        self.run_test_file( test_data_path )
    
    def test__move_cube__top_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube__top_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube__middle_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube__middle_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/move_cube__bottom_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__bottom_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/move_cube__bottom_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube__left_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__left_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube__left_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube__right_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__right_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube__right_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_up_1( self ):
        test_data_path = "tests/test_cases/move_cube__middle_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__move_cube__middle_vertical_down_1( self ):
        test_data_path = "tests/test_cases/move_cube__middle_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM CUBE INPUT TESTS ( function: move_cube ) -------
        
    def test__custom__move_cube__left_vertical_down_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__left_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__left_vertical_up_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__left_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_up_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__right_vertical_up_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__right_vertical_down_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__right_vertical_down_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__top_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__top_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__top_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_right_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__bottom_horizontal_right_1.json" 
        self.run_test_file( test_data_path )

    def test__custom__move_cube__bottom_horizontal_left_1( self ):
        test_data_path = "tests/test_cases/custom__move_cube__bottom_horizontal_left_1.json" 
        self.run_test_file( test_data_path )

    # ------- TEST EVERY POSSIBLE MOVE ( function: rotate_cube ) -------
        
    def test__rotate_cube__left_1( self ):
        test_data_path = "tests/test_cases/rotate_cube__left_1.json" 
        self.run_test_file( test_data_path )

    # ------- CUSTOM CUBE INPUT TESTS ( function: rotate_cube ) -------
        
    def test__custom__rotate_cube_left_1( self ):
        test_data_path = "tests/test_cases/custom__rotate_cube_left_1.json" 
        self.run_test_file( test_data_path )
    



if __name__ == '__main__':
    unittest.main()