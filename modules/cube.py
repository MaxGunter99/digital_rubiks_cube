
from collections import namedtuple
from pprint import pprint
import random
import copy

# I would like to set this up as a 3D Matrix. 
# Perfect to start with but will be scrambled by the algorithm
# random values for colors can not be given manually until later

# OUTPUT ACTIONS
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
        

        # ---------- move_cube util functions ----------

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
            back_side = cube_data[ 3 ]
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

                # 2. slide each left vertical row up
                if given_move.section == "left" and given_move.orientation == "vertical":

                    sides_to_spin = [
                        top_side,
                        front_side,
                        bottom_side if given_move.direction == "up" else bottom_side[::-1],
                        [ i[::-1] for i in back_side ] if given_move.direction == "up" else [ i[::-1] for i in back_side[::-1] ]  # because were reversing it to display correctly, reverse order to keep logic simple
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
                    back_side = [ i[::-1] for i in sides_to_spin[3] ]

                elif given_move.section == "right" and given_move.orientation == "vertical":

                    sides_to_spin = [
                        top_side,
                        front_side,
                        bottom_side if given_move.direction == "up" else bottom_side[::-1],
                        [ i[::-1] for i in back_side ] if given_move.direction == "up" else [ i[::-1] for i in back_side[::-1] ]
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
                            sides_to_spin[ side ][ row ][ shift_index ] = sides_to_spin_static[ next_side ][ row ][ shift_index ]

                    top_side = sides_to_spin[0]
                    front_side = sides_to_spin[1]
                    bottom_side = sides_to_spin[2]
                    back_side = [ i[::-1] for i in sides_to_spin[3] ]

                elif given_move.section == "middle" and given_move.orientation == "vertical":

                    sides_to_spin = [
                        top_side if given_move.direction == "down" else top_side[::-1],
                        front_side,
                        bottom_side if given_move.direction == "up" else bottom_side[::-1],
                        back_side[::-1]
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

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
                    back_side = sides_to_spin[3]

                elif given_move.section == "top" and given_move.orientation == "horizontal":
                    sides_to_spin = [
                        front_side,
                        left_side,
                        back_side,
                        right_side
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

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
                    sides_to_spin = [
                        front_side,
                        left_side,
                        back_side,
                        right_side
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

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

                    sides_to_spin = [
                        front_side,
                        left_side,
                        back_side if given_move.direction == "left" else back_side[::-1], # because were reversing it to display correctly, reverse order to keep logic simple
                        right_side
                    ]
                    sides_to_spin_static = copy.deepcopy( sides_to_spin )

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

        return self.refresh_cube_state( cube_data )

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
                    # print( f"({current_y, current_x}) -> ({row}, {sticker})" )

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

        return self.refresh_cube_state( cube_data )

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

        return
    
    def print_tracked_moves( self ):
        if print_moves == True:
            print("\n Printing moves applied to perfect cube:")
        all_moves_applied = self.tracked_moves
        if len( all_moves_applied ) > 0:
            for move in all_moves_applied:
                print( move )
        return 
        
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