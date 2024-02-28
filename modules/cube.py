
from collections import namedtuple
from pprint import pprint
import copy

# I would like to set this up as a 3D Matrix. 
# Perfect to start with but will be scrambled by the algorithm
# random values for colors can not be given manually until later

# RubiksCube is a class
# but the cube reference is a namedtuple, this enables us to use stuff like:
"""
    cube = RubiksCube()
    cube.top_side
    cube.left_side
    cube.right_side
    cube.front_side
    cube.back_side
    cube.bottom_side
"""

# Named Tuple:
# Cube = namedtuple(
#     'Cube', 
#     [
#         'left_side', 
#         'top_side', 
#         'right_side', 
#         'front_side', 
#         'back_side', 
#         'bottom_side' 
#     ]
# )

Move = namedtuple(
    "Move", 
    [
        "section", 
        "orientation", 
        "direction"
    ]
)

# All algorithm cube transactions need to be using the raw cube values, not meta section names "left_side"

class RubiksCube:
    """
    RubiksCube : Cube
    is a class, but the cube reference is a namedtuple
    so this enables us to use stuff like:

    cube = RubiksCube().cube
    cube.top_side
    cube.left_side
    ...

    OR

    with RubiksCube as rubiks_cube:
        cube = rubiks_cube.cube
        cube.top_side
        cube.left_side
        ...
    
    get cube -> perfect cube
    get cube -> scramble cube -> moves to solve

    if initializing RubiksCube() without supplying a cube
    it will automatically create a new perfect cube
    no need to pass each side, that will be generated on the given cube or the default perfect cube

    """

    def __init__( 
        self
        , cube = None
        , raw_cube = None
    ):

        # Body of the Cube:
        self.cube = cube
        self.raw_cube = raw_cube

        self.left_side = None
        self.top_side = None
        self.right_side = None
        self.front_side = None
        self.back_side = None
        self.bottom_side = None
        
        # If initialized without cube, will start with perfect cube
        cube_supplied = True if cube else False # Extra Cube Attributes
        if not cube:
            details = "No cube data sent, starting with perfect cube"
            print( details )
            new_cube = self.reset_cube()
            self.raw_cube = new_cube
            self.refresh_cube_state()
        elif cube is not None:
            details = f"Starting with custom cube override data! - {cube}"
            print( details )
            self.raw_cube = cube

        # Extra Cube Attributes:
        self.cube_supplied = cube_supplied

    def __getitem__(self, key):
        # Implement the logic to retrieve an item based on the key
        dictionary = {
            "left_side": self.left_side,
            "top_side": self.top_side,
            "right_side": self.right_side,
            "front_side": self.front_side,
            "back_side": self.back_side,
            "bottom_side": self.bottom_side,
            "cube_supplied": self.cube_supplied
        }
        return dictionary[key]

    def reset_cube( 
        self
        , perfect_cube_override = None
    ) :
    # -> Cube:
        """
        returns 3d matrix
        """

        # Imagine a perfect cube on a desk with the white side facing up
        # this data structure is built off of that idea ^

        # perfect_cube = [
        #     #       Left                Top                 Right
        #     [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "w", "w", "w" ], [ "o", "o", "o" ] ],

        #     # Rotate Cube AWAY
        #     #       Left               Front                 Right
        #     [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "b", "b", "b" ], [ "o", "o", "o" ] ],  

        #     # Rotate Cube AWAY
        #     #       Left               Bottom                Right
        #     [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "y", "y", "y" ], [ "o", "o", "o" ] ],   

        #     # Rotate Cube AWAY
        #     #       Left                Back                 Right
        #     [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],
        #     [ [ "r", "r", "r" ], [ "g", "g", "g" ], [ "o", "o", "o" ] ],     
        # ]

        # could use this instead but that would defeat the purpose of this project, 
        # 3d matrix = cube. Lets still get rid of the duplicate sides, 
        # that is just duplicate work that could be prone to errors
        # perfect_cube_json = {
        #     "top": [
        #         [ "w", "w", "w" ],
        #         [ "w", "w", "w" ],
        #         [ "w", "w", "w" ],
        #     ],
        #     "front": [
        #         [ "b", "b", "b" ],
        #         [ "b", "b", "b" ],
        #         [ "b", "b", "b" ],
        #     ],
        #     "bottom": [
        #         [ "y", "y", "y" ],
        #         [ "y", "y", "y" ],
        #         [ "y", "y", "y" ],
        #     ],
        #     "back": [
        #         [ "g", "g", "g" ],
        #         [ "g", "g", "g" ],
        #         [ "g", "g", "g" ],
        #     ],
        #     "left": [
        #         [ "r", "r", "r" ],
        #         [ "r", "r", "r" ],
        #         [ "r", "r", "r" ],
        #     ],
        #     "right": [
        #         [ "o", "o", "o" ]
        #         [ "o", "o", "o" ]
        #         [ "o", "o", "o" ]
        #     ]
        # }

        perfect_cube = [
            # "top": 
            [
                [ "w", "w", "w" ],
                [ "w", "w", "w" ],
                [ "w", "w", "w" ]
            ],
            # "front": 
            [
                [ "b", "b", "b" ],
                [ "b", "b", "b" ],
                [ "b", "b", "b" ]
            ],
            # "bottom": 
            [
                [ "y", "y", "y" ],
                [ "y", "y", "y" ],
                [ "y", "y", "y" ]
            ],
            # "back": 
            [
                [ "g", "g", "g" ],
                [ "g", "g", "g" ],
                [ "g", "g", "g" ]
            ],
            # "left": 
            [
                [ "r", "r", "r" ],
                [ "r", "r", "r" ],
                [ "r", "r", "r" ]
            ],
            # "right": 
            [
                [ "o", "o", "o" ],
                [ "o", "o", "o" ],
                [ "o", "o", "o" ]
            ]
        ]
        #  more manageable right?

        # TODO: Given the raw cube data, we need to add references

        return perfect_cube


    def refresh_cube_state(
        self
        , raw_cube = None
    ):
    # -> Cube:
        """
        Updates cube state!
        raw_cube is new cube data, it will update update all cube state at once
        update -> analyze -> display
        """

        return_value = None
        
        if not raw_cube:
            raw_cube = self.raw_cube

        # print( raw_cube )

        top_side = raw_cube[ 0 ]
        front_side = raw_cube[ 1 ]
        bottom_side = raw_cube[ 2 ]
        back_side = raw_cube[ 3 ]
        left_side = raw_cube[ 4 ]
        right_side = raw_cube[ 5 ]
        
        # formatted_cube = Cube(
        #     left_side,
        #     top_side,
        #     right_side,
        #     front_side,
        #     back_side,
        #     bottom_side,
        # )

        # if formatted_cube:
        # self.cube = formatted_cube
        self.raw_cube = raw_cube
        self.left_side = left_side
        self.top_side = top_side
        self.right_side = right_side
        self.front_side = front_side
        self.back_side = back_side
        self.bottom_side = bottom_side

        return return_value

    def move_cube(
        self,
        section=None,
        orientation=None,
        direction=None,
        turns=0
    ):
        """
        utilizes update_cube_state

        section: "top" "left" "middle" "right" "bottom"
        orientation: "horizontal" "vertical"
        direction: "left" "right" "up" "down"
        turns: turns specified area x times
        """

        # self.cube!
        # cube = self.cube
        raw_cube = self.raw_cube
        updated_raw_cube = None

        if not section or not orientation or not direction or not turns:
            raise Exception( f"missing param in move_cube" )
        
        print( f"Moving the {section} sides {orientation} section {direction}" )
        given_move = Move( section, orientation, direction )

        # section : orientation
        validate_moves = [
            # Move( "top", "horizontal", "left" ),
            # Move( "top", "horizontal", "right" ),
            # Move( "middle", "horizontal", "left" ),
            # Move( "middle", "horizontal", "right" ),
            # Move( "bottom", "horizontal", "left" ),
            # Move( "bottom", "horizontal", "right" ),
            Move( "left", "vertical", "up" ),
            Move( "left", "vertical", "down" ),
            Move( "right", "vertical", "up" ),
            Move( "right", "vertical", "down" ),
            Move( "middle", "vertical", "up" ),
            Move( "middle", "vertical", "down" )
        ]
        # moves list ^
        if given_move not in validate_moves:
            raise Exception( f"Given move not in validate_moves: {section, orientation, direction}" )
        

        # ---------- move_cube util functions ----------

        def spin_side( cube_data, given_move ):
            """
            given the limitations of a cube you are only moving one side at a time 
            ... so we should only need one function for all moves

            only prerequisite is that we need to reformat the cube data to move the right side
            if it is the left side you always want to m

            side_data: cube data [ [], [], [] ]
            direction: left or right
            """

            # "Move", 
            # [
            #     "section", 
            #     "orientation", 
            #     "direction"
            # ]

            # print( given_move.section )
            # print( given_move.direction )

            top_side = cube_data[ 0 ]
            front_side = cube_data[ 1 ]
            bottom_side = cube_data[ 2 ]
            back_side = cube_data[ 3 ]
            left_side = cube_data[ 4 ]
            right_side = cube_data[ 5 ]

            # 1. rotate left side
            # print( f"left side: {left_side}" )

            rotated_side = left_side if given_move.section == "left" else right_side
            rotated_side_index = 4 if rotated_side == "left" else 5
            spin_clockwise = False if ( 
                given_move.section == "left" and given_move.orientation == "vertical" and given_move.direction == "up" 
                or given_move.section == "right" and given_move.orientation == "vertical" and given_move.direction == "down"
            ) else True


            if rotated_side is not None and spin_clockwise is not None:
                print( f"spinning this side: {rotated_side} - clockwise is {spin_clockwise}" )

                new_data = [
                    [],
                    [],
                    [],
                ]

                if given_move.section != "middle":

                    if spin_clockwise == True:

                        current_x = 0
                        current_y = 0

                        for sticker in range( len( rotated_side[0] ) ):
                            min_index = -1
                            iterator = -1
                            for row in range( len( rotated_side ) - 1, min_index, iterator ):
                                print( f"({current_y, current_x}) -> ({row}, {sticker})" )

                                new_data[current_y].append( rotated_side[row][sticker] )

                                current_x += 1 if sticker <= len( rotated_side ) - 1 else 0
                            current_y += 1 if row <= len( rotated_side[0] ) - 1 else 0

                        if given_move.section == "left":
                            left_side = new_data
                        elif given_move.section == "right":
                            right_side = new_data
                        else:
                            raise Exception( "rotated side can not be set, not implemented" )

                    elif spin_clockwise == False:

                        current_x = 0
                        current_y = 0

                        for sticker in range( len( rotated_side[0] ) ):
                            for row in range( len( rotated_side ) - 1, -1, -1 ):

                                print( f"({current_y, current_x}) -> ({row}, {sticker})" )

                                # expect:
                                # ((0, 0)) -> (2, 0)
                                # ((0, 1)) -> (1, 0)
                                # ((0, 2)) -> (0, 0)
                                # ((1, 0)) -> (2, 1)
                                # ((1, 1)) -> (1, 1)
                                # ((1, 2)) -> (0, 1)
                                # ((2, 0)) -> (2, 2)
                                # ((2, 1)) -> (1, 2)
                                # ((2, 2)) -> (0, 2)

                                new_data[row].append( rotated_side[current_y][current_x] )

                                current_x += 1 if current_x < len( rotated_side ) -1 else -current_x
                            current_y += 1 if row <= len( rotated_side[0] ) - 1 else 0

                        if given_move.section == "left":
                            left_side = new_data
                        elif given_move.section == "right":
                            right_side = new_data
                        else:
                            raise Exception( "rotated side can not be set, not implemented" )

                        print( new_data )

                    else:
                        raise Exception("Error spinning side!")

                # 2. slide each left vertical row up
                if given_move.section == "left" and given_move.orientation == "vertical":

                    sides_to_spin = [
                        top_side,
                        front_side,
                        bottom_side,
                        back_side
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

                    shift_index = 0 if given_move.section == "left" else 2
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if spin_clockwise == False:
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0
                        elif spin_clockwise == True:
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ row ][ shift_index ] = sides_to_spin_static[ next_side ][ row ][ shift_index ]

                    top_side = sides_to_spin[0]
                    front_side = sides_to_spin[1]
                    bottom_side = sides_to_spin[2]
                    back_side = sides_to_spin[3]

                elif given_move.section == "right" and given_move.orientation == "vertical":

                    sides_to_spin = [
                        top_side,
                        front_side,
                        bottom_side,
                        back_side
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

                    shift_index = 0 if given_move.section == "left" else 2
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if spin_clockwise == False:
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1
                        elif spin_clockwise == True:
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0
                            
                        for row in range( len( sides_to_spin_static[side] ) ):
                            print(  f"{side} - {row} {shift_index}")
                            sides_to_spin[ side ][ row ][ shift_index ] = sides_to_spin_static[ next_side ][ row ][ shift_index ]

                    top_side = sides_to_spin[0]
                    front_side = sides_to_spin[1]
                    bottom_side = sides_to_spin[2]
                    back_side = sides_to_spin[3]

                # elif given_move.section == "left" and given_move.orientation == "horizontal":
                # elif given_move.section == "right" and given_move.orientation == "horizontal":
                            
                else:
                    raise Exception("Given move not supported!")
                
                # print( raw_cube )
            return [
                top_side,
                front_side,
                bottom_side,
                back_side,
                left_side,
                right_side,
            ]

        # ----------------------------------------------
        
        for _ in range( turns ):

            updated_cube = spin_side( raw_cube, given_move )
        
        return self.refresh_cube_state( updated_cube )


        
    def visualize_cube(self):

        cube = self

        # side_map = [
        #     ( "Left", cube.left_side ),
        #     ( "Top", cube.top_side ),
        #     ( "Right", cube.right_side ),
        #     ( "Front", cube.front_side ),
        #     ( "Back", cube.back_side ),
        #     ( "Bottom", cube.bottom_side )
        # ]

        # PRINT CUBE OUT FOR CLI:
        max_length = " " * len("['w', 'w', 'w']")
        # spacing = " " * len("['w', 'w', 'w']")
        spacing = " " * 1

        def generate_side_str(label, side):
            center_line_length = len("['w', 'w', 'w']")
            centered_word = " " * ( (center_line_length - len(label)) // 2 ) + label + " " * ( (center_line_length - len(label)) // 2 )
            return centered_word, side


        left_label, left_side = generate_side_str( "Left", cube.left_side )
        top_label, top_side = generate_side_str( "Top", cube.top_side )
        right_label, right_side = generate_side_str( "Right", cube.right_side )
        front_label, front_side = generate_side_str( "Front", cube.front_side )
        back_label ,back_side = generate_side_str( "Back", cube.back_side )

        # REVERSE BACKSIDE VALUES BECAUSE OUR DATA STRUCTURE IS NOT A REAL 3D OBJECT
        # referring to the back side of the cube makes you rotate it physically. Were only recording data by spinning around the cube on one axis
        back_side = [ i[::-1] for i in back_side ]

        bottom_label, bottom_side = generate_side_str( "Bottom", cube.bottom_side )


        for data in [
            ( None, None, back_label , back_side,None, None),
            ( left_label, left_side, top_label, top_side, right_label, right_side ),
            ( None, None, front_label, front_side, None, None ),
            ( None, None, bottom_label, bottom_side, None, None ),

        ]:
            (
                side_1_label, 
                side_1_data, 
                side_2_label, 
                side_2_data,
                side_3_label, 
                side_3_data,
            ) = data

            label_str = ""
            label_str += f"\n{side_1_label if side_1_label else max_length}"
            label_str += f"{spacing}"
            label_str += f"{side_2_label if side_2_label else max_length}"
            label_str += f"{spacing}"
            label_str += f"{side_3_label if side_3_label else max_length}"

            base_str = ""
            for i in range(3):
                base_str += f"\n{side_1_data[i] if side_1_data else max_length}"
                base_str += f"{spacing}"
                base_str += f"{side_2_data[i] if side_2_data else max_length}"
                base_str += f"{spacing}"
                base_str += f"{side_3_data[i] if side_3_data else max_length}"

            print( label_str )
            print( base_str )

        print( "\n" )
        return cube