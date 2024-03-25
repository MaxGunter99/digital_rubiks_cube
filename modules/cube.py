
from collections import namedtuple
from pprint import pprint
import random
import copy

# I would like to set this up as a 3D Matrix. 
# Perfect to start with but will be scrambled by the algorithm
# random values for colors can not be given manually until later

# OUTPUT ACTIONS
# print_moves = True
print_moves = False # this is much faster without logging

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
        self.tracked_moves = []
        
        # If initialized without cube, will start with perfect cube
        cube_supplied = True if cube else False # Extra Cube Attributes
        if not cube:
            details = "No cube data sent, starting with perfect cube"
            if print_moves == True:
                print( details )
            new_cube = self.reset_cube()
            self.raw_cube = new_cube
            self.refresh_cube_state(None)
        elif cube is not None:
            details = f"Starting with custom cube override data! - {cube}"
            print( details )
            self.raw_cube = cube
            self.refresh_cube_state(None)

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



    def reset_cube( self ) :
        """
        returns 3d matrix
        """

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

        return perfect_cube



    def refresh_cube_state(
        self
        , raw_cube:list
    ):
    # -> Cube:
        """
        Updates cube state!
        raw_cube is new cube data, it will update update all cube state at once
        update -> analyze -> display
        """

        if print_moves == True:
            print( "... Refreshing cube state!" )
            
        return_value = None
        
        if not raw_cube:
            raw_cube = self.raw_cube

        top_side = raw_cube[ 0 ]
        front_side = raw_cube[ 1 ]
        bottom_side = raw_cube[ 2 ]
        back_side = raw_cube[ 3 ]
        left_side = raw_cube[ 4 ]
        right_side = raw_cube[ 5 ]
        
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

        raw_cube = self.raw_cube

        if not section or not orientation or not direction or not turns:
            raise Exception( f"missing param in move_cube" )
        
        if print_moves == True:
            print( f"Moving the {section} sides {orientation} section {direction} {turns} time(s)" )

        given_move = Move( section, orientation, direction )
        self.tracked_moves.append({
            "action": "move_cube",
            "section": section,
            "orientation": orientation,
            "direction": direction,
            "turns": turns
        })

        # section : orientation
        validate_moves = [
            Move( "top", "horizontal", "left" ),
            Move( "top", "horizontal", "right" ),
            Move( "middle", "horizontal", "left" ),
            Move( "middle", "horizontal", "right" ),
            Move( "bottom", "horizontal", "left" ),
            Move( "bottom", "horizontal", "right" ),
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


        # def spin_side( cube_data, given_move ):
        cube_data = raw_cube
        for _ in range( turns ):
            """
            given the limitations of a cube you are only moving one side at a time 
            ... so we should only need one function for all moves

            only prerequisite is that we need to reformat the cube data to move the right side
            if it is the left side you always want to m

            side_data: cube data [ [], [], [] ]
            direction: left or right
            """

            top_side = cube_data[ 0 ]
            front_side = cube_data[ 1 ]
            bottom_side = cube_data[ 2 ]
            raw_back = cube_data[ 3 ]
            back_side = [ i[::-1] for i in raw_back[::-1] ] if given_move.orientation != "horizontal" else raw_back # reverse & flip back side if using vertical operations
            left_side = cube_data[ 4 ]
            right_side = cube_data[ 5 ]

            rotated_side = None
            if given_move.orientation == "vertical":
                rotated_side = left_side if given_move.section == "left" else right_side
            elif given_move.orientation == "horizontal":
                rotated_side = top_side if given_move.section == "top" else bottom_side

            spin_clockwise = False if ( 
                given_move.section == "left" and given_move.orientation == "vertical" and given_move.direction == "up" 
                or given_move.section == "right" and given_move.orientation == "vertical" and given_move.direction == "down"
                or given_move.section == "top" and given_move.orientation == "horizontal" and given_move.direction == "left" 
                or given_move.section == "bottom" and given_move.orientation == "horizontal" and given_move.direction == "right"
            ) else True


            if rotated_side is not None and spin_clockwise is not None:

                new_data = [
                    [],
                    [],
                    [],
                ]

                # 1. vertical side rotations, left or right side
                if given_move.section != "middle" and given_move.orientation == "vertical":

                    current_x = 0
                    current_y = 0

                    for sticker in range( len( rotated_side[0] ) ):
                        for row in range( len( rotated_side ) - 1, -1, -1 ):

                            if spin_clockwise == True:
                                new_data[current_y].append( rotated_side[row][sticker] )
                                current_x += 1 if sticker <= len( rotated_side ) - 1 else 0
                            elif spin_clockwise == False:
                                new_data[row].append( rotated_side[current_y][current_x] )
                                current_x += 1 if current_x < len( rotated_side ) -1 else -current_x
                            
                        current_y += 1 if row <= len( rotated_side[0] ) - 1 else 0

                    if given_move.section == "left":
                        left_side = new_data
                    elif given_move.section == "right":
                        right_side = new_data
                    else:
                        raise Exception( "rotated side can not be set, not implemented" )
                    
                if given_move.section != "middle" and given_move.orientation == "horizontal":

                    current_x = 0
                    current_y = 0

                    for sticker in range( len( rotated_side[0] ) ):
                        for row in range( len( rotated_side ) -1, -1, -1 ):

                            if spin_clockwise == True:
                                new_data[row].append( rotated_side[current_y][current_x] )
                                current_x += 1 if current_x < len( rotated_side ) -1 else -current_x
                            elif spin_clockwise == False:
                                new_data[current_y].append( rotated_side[row][sticker] )
                                current_x += 1 if sticker <= len( rotated_side ) - 1 else 0
                            
                        current_y += 1 if row <= len( rotated_side[0] ) - 1 else 0

                    if given_move.section == "top":
                        top_side = new_data
                    elif given_move.section == "bottom":
                        bottom_side = new_data
                    else:
                        raise Exception( "rotated side can not be set, not implemented" )



                # 2. slide each vertical/horizontal row up/down/left/right
                if given_move.orientation == "vertical":
                    sides_to_spin = [
                        top_side,
                        front_side,
                        bottom_side,
                        back_side
                    ] 
                
                elif given_move.orientation == "horizontal":
                    sides_to_spin = [
                        front_side,
                        left_side,
                        back_side,
                        right_side
                    ]

                sides_to_spin_static = copy.deepcopy( sides_to_spin )

                if given_move.section == "left" and given_move.orientation == "vertical":

                    shift_index = 0
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
                    back_side = [ i[::-1] for i in ( sides_to_spin[3] )[::-1] ]  # revert initial reverse & flip if using vertical operations

                elif given_move.section == "right" and given_move.orientation == "vertical":

                    shift_index = 2
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if spin_clockwise == False:
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1
                        elif spin_clockwise == True:
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ row ][ shift_index ] = sides_to_spin_static[ next_side ][ row ][ shift_index ]

                    top_side = sides_to_spin[0]
                    front_side = sides_to_spin[1]
                    bottom_side = sides_to_spin[2]
                    back_side = [ i[::-1] for i in ( sides_to_spin[3] )[::-1] ] # revert initial reverse & flip if using vertical operations

                elif given_move.section == "middle" and given_move.orientation == "vertical":

                    shift_index = 1
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if given_move.direction == "down":
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1
                        elif given_move.direction == "up":
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ row ][ shift_index ] = sides_to_spin_static[ next_side ][ row ][ shift_index ]

                    top_side = sides_to_spin[0]
                    front_side = sides_to_spin[1]
                    bottom_side = sides_to_spin[2]
                    back_side = [ i[::-1] for i in ( sides_to_spin[3] )[::-1] ] # revert initial reverse & flip if using vertical operations

                elif given_move.section == "top" and given_move.orientation == "horizontal":

                    shift_index = 0
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if given_move.direction == "left":
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1
                        elif given_move.direction == "right":
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ shift_index ][ row ] = sides_to_spin_static[ next_side ][ shift_index ][ row ]

                    front_side = sides_to_spin[0]
                    left_side = sides_to_spin[1]
                    back_side = sides_to_spin[2]
                    right_side = sides_to_spin[3]
                
                elif given_move.section == "bottom" and given_move.orientation == "horizontal":

                    shift_index = 2
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if given_move.direction == "left":
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1
                        elif given_move.direction == "right":
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ shift_index ][ row ] = sides_to_spin_static[ next_side ][ shift_index ][ row ]

                    front_side = sides_to_spin[0]
                    left_side = sides_to_spin[1]
                    back_side = sides_to_spin[2]
                    right_side = sides_to_spin[3]

                elif given_move.section == "middle" and given_move.orientation == "horizontal":

                    shift_index = 1
                    for side in range( len( sides_to_spin_static ) ):
                        next_side = None
                        if given_move.direction == "left":
                            next_side = side - 1 if side - 1 >= 0 else len( sides_to_spin_static ) - 1

                        elif given_move.direction == "right":
                            next_side = side + 1 if side + 1 < len( sides_to_spin_static ) else 0

                        for row in range( len( sides_to_spin_static[side] ) ):
                            sides_to_spin[ side ][ shift_index ][ row ] = sides_to_spin_static[ next_side ][ shift_index ][ row ]

                    front_side = sides_to_spin[0]
                    left_side = sides_to_spin[1]
                    back_side = sides_to_spin[2]
                    right_side = sides_to_spin[3]
                            
                else:
                    raise Exception("Given move not supported!")
                
            cube_data = [
                top_side,
                front_side,
                bottom_side,
                back_side,
                left_side,
                right_side,
            ]

            if print_moves == True:
                self.refresh_cube_state( raw_cube=cube_data )
                self.visualize_cube()

        return self.refresh_cube_state( raw_cube=cube_data )



    def rotate_cube(
        self,
        direction=None,
        turns=0
    ):
        """
        This function spins the cube in different directions to be able to operate all moves on each side
        you are pushing the front of the cube in which direction?

        direction input options: up, down, left, right
        turns input: int, number of rotations
        """

        direction_options = [ "left", "right", "up", "down" ]
        raw_cube = self.raw_cube

        if direction not in direction_options:
            raise Exception( f"Error rotating cube, direction {direction} is not implemented, available options are {direction_options}" )
        
        if print_moves == True:
            print( f"Rotating cube - {direction} - {turns} time(s)" )

        self.tracked_moves.append({
            "action": "rotate_cube",
            "direction": direction,
            "turns": turns
        })
        
        def spin_side( side_data, spin_clockwise ):
            # print( f"IN ROTATE CUBE - spinning side - {side_data} - clockwise is: {spin_clockwise}" )
            new_data = [
                [],
                [],
                []
            ]
            current_x = 0
            current_y = 0

            for sticker in range( len( side_data[0] ) ):
                for row in range( len( side_data ) - 1, -1, -1 ):

                    if spin_clockwise == True:
                        new_data[current_y].append( side_data[row][sticker] )
                        current_x += 1 if sticker <= len( side_data ) - 1 else 0
                    elif spin_clockwise == False:
                        new_data[row].append( side_data[current_y][current_x] )
                        current_x += 1 if current_x < len( side_data ) -1 else -current_x
                current_y += 1 if row <= len( side_data[0] ) - 1 else 0

            return new_data
        

        cube_data = raw_cube
        for _ in range( turns ):
            top_side = cube_data[0]
            front_side = cube_data[1]
            bottom_side = cube_data[2]
            back_side = cube_data[3]
            left_side = cube_data[4]
            right_side = cube_data[5]
        
            if direction == "left":
                new_top_side = spin_side( top_side, True )
                new_front_side = right_side
                new_bottom_side = spin_side( bottom_side, False )
                new_back_side = left_side
                new_left_side = front_side
                new_right_side = back_side

            elif direction == "right":
                new_top_side = spin_side( top_side, False )
                new_front_side = left_side
                new_bottom_side = spin_side( bottom_side, True )
                new_back_side = right_side
                new_left_side = back_side
                new_right_side = front_side
            
            elif direction == "up":
                new_top_side = front_side
                new_front_side = bottom_side
                new_bottom_side = [ i[::-1] for i in back_side[::-1] ]
                new_back_side = [ i[::-1] for i in top_side[::-1] ]
                new_left_side = spin_side( left_side, False )
                new_right_side = spin_side( right_side, True )

            elif direction == "down":
                new_top_side = [ i[::-1] for i in back_side[::-1] ]
                new_front_side = top_side
                new_bottom_side = front_side
                new_back_side = [ i[::-1] for i in bottom_side[::-1] ]
                new_left_side = spin_side( left_side, True )
                new_right_side = spin_side( right_side, False )

            else:
                raise Exception( "Rotation direction not implemented" )
            
            cube_data = [
                new_top_side,
                new_front_side,
                new_bottom_side,
                new_back_side,
                new_left_side,
                new_right_side
            ]

            if print_moves == True:
                self.refresh_cube_state( raw_cube=cube_data )
                self.visualize_cube()

        return self.refresh_cube_state( raw_cube=cube_data )



    def shuffle_cube( 
        self, 
        random_turns_count:int=0 ,
        disable_rotations:bool=False
    ):
        """
        This will shuffle the cube given any number of turns
        """
        if random_turns_count == 0:
            details = "random_turns_count is 0, not shuffling the cube"
            print(details)
            return details
        
        if print_moves == True:
            print( "\nShuffling cube!!" )

        all_possible_moves = [
            [ "top", "horizontal", "left" ],
            [ "top", "horizontal", "right" ],
            [ "middle", "horizontal", "left" ],
            [ "middle", "horizontal", "right" ],
            [ "bottom", "horizontal", "left" ],
            [ "bottom", "horizontal", "right" ],
            [ "left", "vertical", "up" ],
            [ "left", "vertical", "down" ],
            [ "right", "vertical", "up" ],
            [ "right", "vertical", "down" ],
            [ "middle", "vertical", "up" ],
            [ "middle", "vertical", "down" ]
        ]
        all_possible_rotations = [ "left", "right", "up", "down" ]

        for _ in range( random_turns_count ):

            # define chance to rotate before making a random move
            # 4 is 25% chance
            # 2 is 50% chance
            chance_to_rotate = 2
            random_number = random.randrange( 0, 100 )
            
            if disable_rotations == False and random_number % chance_to_rotate == 0:
                rotate_direction = random.choices( all_possible_rotations )[0]
                rotate_turns = random.randrange( 1, 3 )
                self.rotate_cube( rotate_direction, rotate_turns )

            move_data = random.choices( all_possible_moves )[0]
            move_turns = random.randrange( 1, 3 )
            move_section, move_orientation, move_direction = move_data
            self.move_cube( move_section, move_orientation, move_direction, move_turns )

        return True
    
    # given a sticker on a side, I need to know if the attached colors match that side
    def read_brick( self, side_name, row_index, sticker_index ):
        """
        this generates prick data in json format, it will return details about each brick along with the parent information
        """

        # config tells us what side data to grab given a side_name, row_index, and sticker_index
        # TODO: improve this in the future, this is hard coded
        side_relationship_mappings = {
            "top_side": [ 

                # TOP ROW
                [
                    [ ( "left_side", 0, 0 ), ( "back_side", 0, 2 )],
                    [ ( "back_side", 0, 1 ) ],
                    [ ( "left_side", 0, 2 ), ( "back_side", 0, 0 ) ],
                ],

                # MIDDLE ROW
                [
                    [ ( "left_side", 0, 1 ) ],
                    [ ( "top_side", 1, 1 ) ],
                    [ ( "right_side", 0, 1 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "left_side", 0, 2 ), ( "front_side", 0, 0 ) ],
                    [ ( "front_side", 0, 1 ) ],
                    [ ( "right_side", 0, 0 ), ( "front_side", 0, 2 ) ]
                ]
            ],
            "front_side": [ 
                # TOP ROW
                [
                    [ ( "top_side", 2, 0 ), ( "left_side", 0, 2 ) ],
                    [ ( "top_side", 2, 1 ) ],
                    [ ( "right_side", 0, 0 ), ( "top_side", 2, 2 ) ],
                ],
                
                # MIDDLE ROW
                [
                    [ ( "left_side", 1, 2 ) ],
                    [ ( "front_side", 1, 1 ) ],
                    [ ( "right_side", 1, 0 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "left_side", 2, 2 ), ( "bottom_side", 0, 0 ) ],
                    [ ( "bottom_side", 0, 1 ) ],
                    [ ( "right_side", 0, 0 ), ( "bottom_side", 0, 2 ) ]
                ]
            ],
            "bottom_side": [ 

                # TOP ROW
                [
                    [ ( "front_side", 2, 0 ), ( "left_side", 2, 2 ) ],
                    [ ( "front_side", 2, 1 ) ],
                    [ ( "right_side", 2, 0 ), ( "front_side", 2, 2 ) ],
                ],
                
                # MIDDLE ROW
                [
                    [ ( "left_side", 2, 1 ) ],
                    [ ( "bottom_side", 1, 1 ) ],
                    [ ( "right_side", 2, 1 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "left_side", 2, 0 ), ( "back_side", 2, 2 ) ],
                    [ ( "back_side", 2, 1 ) ],
                    [ ( "back_side", 2, 0 ), ( "right_side", 2, 2 ) ]
                ]
            ],
            "back_side": [ 

                # TOP ROW
                [
                    [ ( "top_side", 0, 2 ), ( "right_side", 0, 2 ) ],
                    [ ( "top_side", 0, 1 ) ],
                    [ ( "top_side", 0, 0 ), ( "left_side", 0, 0 ) ],
                ],
                
                # MIDDLE ROW
                [
                    [ ( "right_side", 1, 2 ) ],
                    [ ( "back_side", 1, 1 ) ],
                    [ ( "left_side", 1, 0 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "bottom_side", 2, 2 ), ( "right_side", 2, 2 ) ],
                    [ ( "bottom_side", 2, 1 ) ],
                    [ ( "bottom_side", 2, 0 ), ( "left_side", 2, 0 ) ]
                ]
            ],
            "left_side": [ 

                # TOP ROW
                [
                    [ ( "back_side", 0, 2 ), ( "top_side", 0, 0 ) ],
                    [ ( "top_side", 1, 0 ) ],
                    [ ( "top_side", 2, 0 ), ( "front_side", 0, 0 ) ],
                ],
                
                # MIDDLE ROW
                [
                    [ ( "back_side", 1, 2 ) ],
                    [ ( "left_side", 1, 1 ) ],
                    [ ( "front_side", 1, 0 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "back_side", 2, 2 ), ( "bottom_side", 2, 0 ) ],
                    [ ( "bottom_side", 1, 0 ) ],
                    [ ( "bottom_side", 0, 0 ), ( "front_side", 2, 0 ) ]
                ]
            ],
            "right_side": [ 

                # TOP ROW
                [
                    [ ( "top_side", 2, 2 ), ( "front_side", 0, 2 ) ],
                    [ ( "top_side", 1, 2 ) ],
                    [ ( "top_side", 0, 2 ), ( "back_side", 0, 0 ) ],
                ],
                
                # MIDDLE ROW
                [
                    [ ( "front_side", 1, 2 ) ],
                    [ ( "right_side", 1, 1 ) ],
                    [ ( "back_side", 1, 0 ) ],
                ],

                # BOTTOM ROW
                [
                    [ ( "front_side", 2, 2 ), ( "bottom_side", 0, 2 ) ],
                    [ ( "bottom_side", 1, 2 ) ],
                    [ ( "bottom_side", 2, 2 ), ( "back_side", 2, 0 ) ]
                ]
            ]
        }
        check_brick_relationships = side_relationship_mappings[side_name][row_index][sticker_index]
        related_values = {}
        parent_value = self[side_name][row_index][sticker_index]
        parent_center_color = self[side_name][1][1]
        parent_matches_side_center = parent_value == parent_center_color
        related_values["parent_data"] = {
            "parent_side": side_name,
            "parent_row_index": row_index,
            "parent_sticker_index": sticker_index,
            "parent_value": parent_value,
            "matches_side": parent_matches_side_center,
        }
        cube_in_place = False
        for related_side_name, related_row_index, related_sticker_index in check_brick_relationships:
            related_side_data = self[related_side_name]
            related_value = related_side_data[related_row_index][related_sticker_index]
            related_side_center = related_side_data[1][1]
            matches_side_center = related_side_center == related_value
                
            # only include parent data if its a center piece
            if ( row_index, sticker_index ) != ( 1, 1 ):
                related_values[related_side_name] = {
                    "row_index": related_row_index,
                    "related_sticker_index": related_sticker_index,
                    "value": related_value,
                    "matches_side": matches_side_center,
                }
            cube_in_place = matches_side_center
        # print( side_name, related_values )
        return related_values, cube_in_place

    def check_sides( self, color_search=None ):
        """
        this returns how many pieces per side match that side
        a perfect cube should return this
        {
            'bottom_side': {'brick_data': {...}, 'cubes_in_place': 9},
            'front_side': {'brick_data': {...}, 'cubes_in_place': 9},
            'left_side': {'brick_data': {...}, 'cubes_in_place': 9},
            'right_side': {'brick_data': {...}, 'cubes_in_place': 9},
            'top_side': {'brick_data': {...}, 'cubes_in_place': 9}
        }
        cubes_in_place minimum is always 1, the center brick
        if you pass color_search, it will only return data for that side value
        ex: you are trying find all of the 'g' pieces and their related side data

        passing related_colors_search will only include color_search pieces with attached related_colors_search
        """

        return_data = {}
        best_side_name = None # this is where to start
        best_side_value = None

        for side_name in ["top_side", "front_side", "bottom_side", "back_side", "left_side", "right_side"]:
            current_side = self[side_name]
            current_side_center = current_side[1][1]
            cubes_in_place = 0
            collected_data = []

            for row_index in range( len( current_side ) ):
                for sticker_index in range( len( current_side[ row_index ] ) ):
                    sticker_value = current_side[ row_index ][ sticker_index ]

                    if color_search is not None and sticker_value != color_search:
                        pass

                    elif (
                        color_search is not None and sticker_value == color_search
                        or color_search is None and sticker_value == current_side_center
                    ):
                        brick_data, cube_in_place = self.read_brick( side_name, row_index, sticker_index )
                        if cube_in_place:
                            cubes_in_place += 1
                        collected_data.append( brick_data )


            # tracking what side has the most cubes in place, a good starting point
            if collected_data != []:
                return_data[side_name] = {
                    "brick_data": collected_data,
                    "cubes_in_place": cubes_in_place
                }
            if best_side_value == None or cubes_in_place > best_side_value:
                best_side_name = side_name
                best_side_value = cubes_in_place

        return_data["best_side_data"] = {
            "side_name": best_side_name,
            "cubes_in_place": best_side_value
        }

        # pprint( return_data, depth=2 )
        # print( best_side_name, best_side_value )
        return return_data





    def solve_cube( self , step_override=None ):
        """
        This function should output a list of moves to solve the cube. 
        step format: [ class_function, args ]
        real example: [ 'rotate_cube', 'up', 1 ]

        we need to:
            1. determine what steps have already been completed on the cube, lets write some real tests, TDD
            2. We need a solve loop that will perform each step of the solve process
        """

        steps_to_solve = []

        print( "initial cube" )
        self.visualize_cube()

        step_1_status = "FAIL"

        if step_override == None or step_override == 1:

            print( "Starting Step 1!" )
            step_1_errors = []
            # what do we want to assert? What were testing, the top cross needs to be solved
            # run check cube function to find the side with the most matching pieces, we can find this in best_side_data
            # 'best_side_data': {'side_name': 'top_side', 'cubes_in_place': 9}

            # if this is the top_side keep it there, if not rotate the cube to get the best side_name to the top
            # how does step 1 pass? the best_side_name needs to == top_side
            cube_analysis = self.check_sides()
            best_side_data = cube_analysis.get( "best_side_data" )
            best_side_name = best_side_data.get( "side_name" )

            # print( f"initial best_side_data: {best_side_data}" )

            if best_side_name != "top_side":
                rotation_mapping = {
                    "front_side": [ ("up", 1) ],
                    "back_side": [ ("down", 1) ],
                    "left_side": [ ("right", 1), ("up", 1) ],
                    "right_side": [ ("left", 1), ("up", 1) ],
                    "bottom_side": [ ("up", 2) ]
                }
                steps_to_pass = rotation_mapping.get( best_side_name )
                for direction, turns in steps_to_pass:
                    self.rotate_cube( direction, turns )
                    step_data = ["rotate_cube", direction, turns]
                    steps_to_solve.append( step_data )

                    # re-run cube analysis function
                    updated_cube_analysis = self.check_sides()
                    best_side_data = updated_cube_analysis.get( "best_side_data" )
                    best_side_name = best_side_data.get( "side_name" )

            if best_side_name != "top_side":
                details = f"Step 1: best side needs to be top_side, it is returning: {best_side_name}"
                step_1_errors.append( details )

            # what if we have a mixed cube?
            # what pieces need to be moved?
            # can this be found on the cube analysis?
            # you need to find all of the pieces you are trying to solve for with their related data
            # what value do we need to find?
                
            # test for matching 
            # self.move_cube( "top", "horizontal", "left", 1 )

            # find all 4 cross pieces, where are they?


            # after every move we will need to update data locations
            def refresh_data():

                print( "REFRESHING DATA" )
                top_indexes_to_fix = {
                    # row, index: is_perfect
                    ( 0, 1 ): False,
                    ( 1, 0 ): False,
                    ( 1, 2 ): False,
                    ( 2, 1 ): False
                }
                top_color_value = self.top_side[1][1]
                top_color_locations = self.check_sides( top_color_value )
                top_row_pieces = []
                middle_row_pieces = []
                bottom_row_pieces = []

                for side_name, side_data in top_color_locations.items():
                    # print( f"Checking this sides data: {side_name}" )

                    if side_name == "best_side_data":
                        continue

                    sides_brick_data = side_data.get("brick_data")

                    for color_data in sides_brick_data:
                        # length of 2
                        # parent containing top_color_value
                        if len( color_data ) == 2:

                            # if both colors match the sides center, ie matches_side == True for parent and related sides then we should not move them
                            brick_is_perfect = True if False not in [ color_data[i]["matches_side"] for i in color_data.keys() ] else False
                            # print( f"brick_is_perfect??? {brick_is_perfect}" )
                            bricks_parent_data = color_data["parent_data"]

                            # if brick_is_perfect:
                            bricks_parent_side = bricks_parent_data.get("parent_side")
                            bricks_parent_row = bricks_parent_data.get("parent_row_index")
                            bricks_parent_sticker = bricks_parent_data.get("parent_sticker_index")
                            top_indexes_to_fix[ ( bricks_parent_row, bricks_parent_sticker ) ] = brick_is_perfect

                            if not brick_is_perfect:
                                # sorting pieces if they are not perfect
                                parent_side = bricks_parent_data.get("parent_side")
                                if (
                                    parent_side == "top_side"
                                    or bricks_parent_side in [ "front_side", "back_side", "left_side", "right_side" ] and bricks_parent_row == 0
                                ):
                                    top_row_pieces.append( color_data )

                                elif (
                                    "front_side" in color_data.keys() and color_data["front_side"]["row_index"] == 1
                                    or "back_side" in color_data.keys() and color_data["back_side"]["row_index"] == 1
                                    or "left_side" in color_data.keys() and color_data["left_side"]["row_index"] == 1
                                    or "right_side" in color_data.keys() and color_data["right_side"]["row_index"] == 1
                                ):
                                    middle_row_pieces.append( color_data )

                                elif (
                                    parent_side == "bottom_side"
                                    or "front_side" in color_data.keys() and color_data["front_side"]["row_index"] == 2
                                    or "back_side" in color_data.keys() and color_data["back_side"]["row_index"] == 2
                                    or "left_side" in color_data.keys() and color_data["left_side"]["row_index"] == 2
                                    or "right_side" in color_data.keys() and color_data["right_side"]["row_index"] == 2
                                ):
                                    bottom_row_pieces.append( color_data )
                                else:
                                    raise Exception( f"Unsorted piece while sorting into rows: {color_data}" )

                return ( top_row_pieces, middle_row_pieces, bottom_row_pieces, top_indexes_to_fix )
            
            # change this to 
            game_loop_max_count = 5
            game_loop_iteration = 0
            game_loop_complete = False

            while (
                game_loop_max_count < 10 
                or game_loop_complete == False and game_loop_iteration < game_loop_max_count
            ): 
                game_loop_iteration += 1
                print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
                self.visualize_cube()

                if game_loop_iteration >= game_loop_max_count:
                    break

                top_row_pieces, middle_row_pieces, bottom_row_pieces, top_indexes_to_fix = refresh_data()

                game_loop_complete_check = [ is_perfect for _, is_perfect in top_indexes_to_fix.items() ]
                if False not in game_loop_complete_check:
                    print("COMPLETE")
                    game_loop_complete = True
                    break

                # print( f"top_indexes_to_fix: {top_indexes_to_fix}" )
                # print( f"top_row_pieces: {top_row_pieces}" )
                # print( f"middle_row_pieces: {middle_row_pieces}" )
                # print( f"bottom_row_pieces: {bottom_row_pieces}" )
                # next, if you can match any of the top sides to their matching side
                # do that before moving any side or bottom pieces  
                        
                # TOP ROW

                # lets fix one at a time
                if len( top_row_pieces ) >= 1:
                    
                    print( "\nFixing top piece" )

                    piece = top_row_pieces[0]
                    print( piece )
                    piece_side = [ key for key in piece.keys() if key != "parent_data" ][0]
                    piece_color = piece[ piece_side ][ "value" ]
                    piece_parent_data = piece.get("parent_data")
                    parent_side = piece_parent_data.get("parent_side")
                    parent_color = piece_parent_data.get("parent_value")

                    to_side_mappings = {
                        self.front_side[1][1]: "front_side",
                        self.back_side[1][1]: "back_side",
                        self.left_side[1][1]: "left_side",
                        self.right_side[1][1]: "right_side"
                    } 
                    from_to_move_config = {
                        ( "front_side", "left_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 1 )],
                        ( "front_side", "right_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 1 )],
                        ( "front_side", "back_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 2 )],

                        ( "left_side", "right_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 2 )],
                        ( "left_side", "back_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 1 )],
                        ( "left_side", "front_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 1 )],

                        ( "back_side", "right_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 1 )],
                        ( "back_side", "front_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 2 )],
                        ( "back_side", "left_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 1 )],

                        ( "right_side", "back_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 1 )],
                        ( "right_side", "front_side", "top_side" ): [( "move_cube", "top", "horizontal", "right", 1 )],
                        ( "right_side", "left_side", "top_side" ): [( "move_cube", "top", "horizontal", "left", 2 )],

                        ( "top_side", "back_side", "front_side" ): [
                            ( "rotate_cube", "right", 1 ),
                            ( "move_cube", "right", "vertical", "up", 1 ),
                            ( "rotate_cube", "left", 1 ),
                            ( "move_cube", "top", "horizontal", "left", 1 ),
                            ( "move_cube", "right", "vertical", "up", 1 ),
                            ( "move_cube", "top", "horizontal", "right", 1 ),
                        ],

                    }

                    # if the correct color is already on top, just need to rotate top
                    if parent_color == self.top_side[1][1]:

                        # where do we need to end up
                        move_from_to = ( piece_side, to_side_mappings[ piece_color ], parent_side )

                        if move_from_to not in from_to_move_config:
                            raise Exception( f"Sorting top cross piece is not supported! - {move_from_to}" )
                        
                        required_moves = from_to_move_config[ move_from_to ]

                        for move in required_moves:
                            print( move )
                            if move[0] == "rotate_cube":
                                _, direction, turns = move
                                self.rotate_cube( direction, turns )
                                steps_to_solve.append( ["rotate_cube", direction, turns] )

                            elif move[0] == "move_cube": 
                                _, section, orientation, direction, turns = move
                                self.move_cube( section, orientation, direction, turns )
                                steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )

                        continue

                    else:
                        # TODO: write a tests where white is on the side of a top piece
                        raise Exception( "Solve for top row not implemented yet!" )

                elif (
                    len( top_row_pieces ) == 0
                    and len( middle_row_pieces ) >= 1
                ):
                    print( "\nFixing middle piece" )

                    piece = middle_row_pieces[0]
                    piece_side = [ key for key in piece.keys() if key != "parent_data" ][0]
                    piece_color = piece[ piece_side ][ "value" ]
                    piece_parent_data = piece.get("parent_data")
                    parent_color = piece_parent_data.get("parent_value")
                    parent_side = piece_parent_data.get("parent_side")
                    parent_sticker_index = piece_parent_data.get("parent_sticker_index")

                    to_side_mappings = {
                        self.front_side[1][1]: "front_side",
                        self.back_side[1][1]: "back_side",
                        self.left_side[1][1]: "left_side",
                        self.right_side[1][1]: "right_side"
                    } 
                    from_to_move_config = {

                        ( "left_side", "top_side", 1 ): [ ( "rotate_cube", "right", 1 ), ( "move_cube", "left", "vertical", "up", 1 ) ],
                        ( "left_side", "top_side", 2 ): [ ( "rotate_cube", "right", 1 ), ( "move_cube", "right", "vertical", "up", 1 ) ],

                        ( "right_side", "top_side", 1 ): [ ( "rotate_cube", "left", 1 ), ( "move_cube", "left", "vertical", "up", 1 ) ],
                        ( "right_side", "top_side", 2 ): [ ( "rotate_cube", "left", 1 ), ( "move_cube", "right", "vertical", "up", 1 ) ],

                        ( "back_side", "top_side", 1 ): [ ( "move_cube", "right", "vertical", "down", 1 ) ],
                        ( "back_side", "top_side", 2 ): [ ( "move_cube", "left", "vertical", "down", 1 ) ],

                        ( "front_side", "top_side", 1 ): [ ( "move_cube", "left", "vertical", "up", 1 ) ],
                        ( "front_side", "top_side", 2 ): [ ( "move_cube", "right", "vertical", "up", 1 ) ],
                    }
                    destination_side = "top_side"
                    move_from_to = ( parent_side, destination_side, parent_sticker_index )
                    required_moves = from_to_move_config[ move_from_to ]

                    for move in required_moves:
                        print( move )
                        if move[0] == "rotate_cube":
                            _, direction, turns = move
                            self.rotate_cube( direction, turns )
                            steps_to_solve.append( ["rotate_cube", direction, turns] )

                        elif move[0] == "move_cube": 
                            _, section, orientation, direction, turns = move
                            self.move_cube( section, orientation, direction, turns )
                            steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )

                    continue

                elif (
                    len( top_row_pieces ) == 0
                    and len( middle_row_pieces ) == 0
                    and len( bottom_row_pieces ) >= 1
                ):
                    print( "\nFixing bottom piece" )
                    break

                else:
                    break
                    # self.visualize_cube()
                    # raise Exception("No pieces to fix!")
                
            # ------- GAME LOOP END

            if len( step_1_errors ):
                print( f"Errors in step 1: {step_1_errors}" )
                raise Exception( f"Errors in step 1: {step_1_errors}" )
            else:
                step_1_status = "PASS" if False not in [ is_perfect for _, is_perfect in top_indexes_to_fix.items() ] else "FAIL"

        print({
            "step_1_status": step_1_status
        })
        print(f"steps_to_solve: {steps_to_solve}")
        self.visualize_cube()
        return steps_to_solve
    


    def print_tracked_moves( self ):
        if print_moves == True:
            print("\n Printing moves applied to perfect cube:")
        all_moves_applied = self.tracked_moves
        if len( all_moves_applied ) > 0:
            for move in all_moves_applied:
                print( move )
        return True
        
    def visualize_cube(self):

        # PRINT CUBE OUT FOR CLI:
        max_length = " " * len("['w', 'w', 'w']")
        spacing = " "

        def generate_side_str(label, side):
            center_line_length = len("['w', 'w', 'w']")
            centered_word = " " * ( (center_line_length - len(label)) // 2 ) + label + " " * ( (center_line_length - len(label)) // 2 )
            return centered_word, side


        left_label, left_side = generate_side_str( "Left", self.left_side )
        top_label, top_side = generate_side_str( "Top", self.top_side )
        right_label, right_side = generate_side_str( "Right", self.right_side )
        front_label, front_side = generate_side_str( "Front", self.front_side )
        back_label ,back_side = generate_side_str( "Back", self.back_side )
        bottom_label, bottom_side = generate_side_str( "Bottom", self.bottom_side )


        for data in [
            ( None, None, back_label , back_side,None, None),
            ( None, None, top_label, top_side, None, None ),
            ( left_label, left_side, front_label, front_side, right_label, right_side ),
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
        return