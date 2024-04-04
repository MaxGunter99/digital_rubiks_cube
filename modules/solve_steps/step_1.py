
# STEP 1

def solve_cube__step_1( cube_client, test_id=None ):
    """
    This function should output a list of moves to solve the top cross of the cube. 
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

    DESCRIPTION:
        Solve the top cross:
            It needs to be rotated up from one of these sides, left, right, front, back.
            May require turning the top side into the correct spot, will need to rotate back.

    OVERVIEW:     
        We need to:
            1. determine what steps have already been completed on the cube, lets write some real tests, TDD
            2. We need a solve loop that will perform each step of the solve process
    """

    steps_to_solve=[]
    step_1_status = "FAIL"

    print( "Starting Step 1!" )
    step_1_errors = []
    # what do we want to assert? What were testing, the top cross needs to be solved
    # run check cube function to find the side with the most matching pieces, we can find this in best_side_data
    # 'best_side_data': {'side_name': 'top_side', 'cubes_in_place': 9}

    # if this is the top_side keep it there, if not rotate the cube to get the best side_name to the top
    # how does step 1 pass? the best_side_name needs to == top_side
    cube_analysis = cube_client.check_sides()
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
        print( f"Rotating cube to move best side to the top. {best_side_name} -> top_side" )
        for direction, turns in steps_to_pass:
            cube_client.rotate_cube( direction, turns )
            step_data = ["rotate_cube", direction, turns]
            steps_to_solve.append( step_data )

            # re-run cube analysis function
            updated_cube_analysis = cube_client.check_sides()
            best_side_data = updated_cube_analysis.get( "best_side_data" )
            best_side_name = best_side_data.get( "side_name" )

        cube_client.visualize_cube()

    if best_side_name != "top_side":
        details = f"Step 1: best side needs to be top_side, it is returning: {best_side_name}"
        step_1_errors.append( details )

    # what if we have a mixed cube?
    # what pieces need to be moved?
    # can this be found on the cube analysis?
    # you need to find all of the pieces you are trying to solve for with their related data
    # what value do we need to find?
        
    # test for matching 
    # cube_client.move_cube( "top", "horizontal", "left", 1 )

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
        top_color_value = cube_client.top_side[1][1]
        top_color_locations = cube_client.check_sides( top_color_value )
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
                    bricks_parent_side = bricks_parent_data.get("parent_side")
                    bricks_parent_row = bricks_parent_data.get("parent_row_index")
                    bricks_parent_sticker = bricks_parent_data.get("parent_sticker_index")
                    color_data_side = color_data.get("side")
                    top_indexes_to_fix[ ( bricks_parent_row, bricks_parent_sticker ) ] = brick_is_perfect

                    if not brick_is_perfect:
                        # sorting pieces if they are not perfect
                        if (
                            bricks_parent_side == "top_side"
                            or bricks_parent_side in [ "front_side", "back_side", "left_side", "right_side" ] 
                            and bricks_parent_row == 0
                        ):
                            top_row_pieces.append( color_data )

                        elif (
                            bricks_parent_side in [ "front_side", "back_side", "left_side", "right_side" ]
                            and bricks_parent_row == 1
                        ):
                            middle_row_pieces.append( color_data )

                        elif (
                            bricks_parent_side == "bottom_side"
                            or bricks_parent_side in [ "front_side", "back_side", "left_side", "right_side" ] 
                            and bricks_parent_row == 2
                        ):
                            bottom_row_pieces.append( color_data )
                        else:
                            raise Exception( f"Unsorted piece while sorting into rows: {color_data}" )

        return ( top_row_pieces, middle_row_pieces, bottom_row_pieces, top_indexes_to_fix )
        
    # change this to 
    game_loop_max_count = 10
    game_loop_iteration = 0
    game_loop_complete = False

    while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ): 
        game_loop_iteration += 1
        print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )

        cube_client.visualize_cube()

        if game_loop_iteration >= game_loop_max_count:
            break

        top_row_pieces, middle_row_pieces, bottom_row_pieces, top_indexes_to_fix = refresh_data()

        game_loop_complete_check = [ is_perfect for _, is_perfect in top_indexes_to_fix.items() ]
        if False not in game_loop_complete_check:
            print("COMPLETE")
            game_loop_complete = True
            break

        # print( f"top_indexes_to_fix: {top_indexes_to_fix}" )
        print( f"top_row_pieces: {top_row_pieces}" )
        print( f"middle_row_pieces: {middle_row_pieces}" )
        print( f"bottom_row_pieces: {bottom_row_pieces}" )
        # next, if you can match any of the top sides to their matching side
        # do that before moving any side or bottom pieces  
                
        # TOP ROW

        # lets fix one at a time
        if len( top_row_pieces ) >= 1:
            print( "\nFixing top piece" )

            piece = top_row_pieces[0]
            piece_side = [ key for key in piece.keys() if key != "parent_data" ][0]
            piece_color = piece[ piece_side ][ "value" ]
            piece_parent_data = piece.get("parent_data")
            parent_color = piece_parent_data.get("parent_value")
            parent_side = piece_parent_data.get("parent_side")
            parent_row_index = piece_parent_data.get("parent_row_index")
            parent_sticker_index = piece_parent_data.get("parent_sticker_index")

            to_side_mappings = {
                cube_client.front_side[1][1]: "front_side",
                cube_client.back_side[1][1]: "back_side",
                cube_client.left_side[1][1]: "left_side",
                cube_client.right_side[1][1]: "right_side"
            } 
            # The parent is always the solve color, were just matching the sides
            # Format: ( piece_color, color_destination_side, parent_side )
            from_to_move_config = {
                ('front_side', 0, 1, 'front_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'left', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('left_side', 1, 0, 'back_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('rotate_cube', 'left', 1)],
                ('top_side', 0, 1, 'left_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'left', 'vertical', 'down', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'left', 1)],
            }

            # if the correct color is already on top, just need to rotate top
            if parent_color == cube_client.top_side[1][1]:

                # where do we need to end up
                destination_side = "top_side"
                move_from_to = ( parent_side, parent_row_index, parent_sticker_index, to_side_mappings[ piece_color ], destination_side )
                print( move_from_to )
                if move_from_to not in from_to_move_config:
                    details = f"Sorting top cross piece is not supported! - {move_from_to}"
                    print( details )
                    cube_client.visualize_cube()
                    raise Exception( details )
                
                required_moves = from_to_move_config[ move_from_to ]

                for move in required_moves:
                    print( move )
                    if move[0] == "rotate_cube":
                        _, direction, turns = move
                        cube_client.rotate_cube( direction, turns )
                        steps_to_solve.append( ["rotate_cube", direction, turns] )

                    elif move[0] == "move_cube": 
                        _, section, orientation, direction, turns = move
                        cube_client.move_cube( section, orientation, direction, turns )
                        steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )

                continue

            else:
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
            parent_row_index = piece_parent_data.get("parent_row_index")
            parent_sticker_index = piece_parent_data.get("parent_sticker_index")

            to_side_mappings = {
                cube_client.front_side[1][1]: "front_side",
                cube_client.back_side[1][1]: "back_side",
                cube_client.left_side[1][1]: "left_side",
                cube_client.right_side[1][1]: "right_side"
            } 
            from_to_move_config = {
                ('back_side', 1, 0, 'left_side', 'top_side'): [('move_cube', 'middle', 'horizontal', 'right', 2), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'middle', 'horizontal', 'left', 2)],
                ('back_side', 1, 0, 'right_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'down', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('rotate_cube', 'left', 1)],
                ('back_side', 1, 2, 'left_side', 'top_side'): [('move_cube', 'left', 'vertical', 'down', 1)],
                ('front_side', 1, 0, 'left_side', 'top_side'): [('move_cube', 'left', 'vertical', 'up', 1)],
                ('front_side', 1, 2, 'left_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'right', 2), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 2)],
                ('front_side', 1, 2, 'right_side', 'top_side'): [('move_cube', 'right', 'vertical', 'up', 1)],
                ('left_side', 1, 0, 'left_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'left', 1)],
                ('left_side', 1, 2, 'left_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('rotate_cube', 'left', 1)],
                ('right_side', 1, 0, 'left_side', 'top_side'): [('move_cube', 'middle', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'middle', 'horizontal', 'right', 1)],
                ('right_side', 1, 2, 'left_side', 'top_side'): [('move_cube', 'middle', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'down', 1), ('move_cube', 'middle', 'horizontal', 'left', 1)],
            }
            destination_side = "top_side"
            # move_from_to = ( parent_side, destination_side, parent_sticker_index )
            move_from_to = ( parent_side, parent_row_index, parent_sticker_index, to_side_mappings[ piece_color ], destination_side )
            print( move_from_to )

            print( sorted( from_to_move_config ) )
            for key in sorted( from_to_move_config ):
                print( f"{key}: {from_to_move_config[key]}" )
            
            if move_from_to not in from_to_move_config:
                details = f"Sorting top cross piece is not supported! - {move_from_to}"
                print( details )
                cube_client.visualize_cube()
                raise Exception( details )
            
            required_moves = from_to_move_config[ move_from_to ]

            for move in required_moves:
                print( move )
                if move[0] == "rotate_cube":
                    _, direction, turns = move
                    cube_client.rotate_cube( direction, turns )
                    steps_to_solve.append( ["rotate_cube", direction, turns] )

                elif move[0] == "move_cube": 
                    _, section, orientation, direction, turns = move
                    cube_client.move_cube( section, orientation, direction, turns )
                    steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )

            continue

        elif (
            len( top_row_pieces ) == 0
            and len( middle_row_pieces ) == 0
            and len( bottom_row_pieces ) >= 1
        ):
            print( "\nFixing bottom piece" )

            piece = bottom_row_pieces[0]
            piece_side = [ key for key in piece.keys() if key != "parent_data" ][0]
            piece_color = piece[ piece_side ][ "value" ]
            piece_parent_data = piece.get("parent_data")
            parent_color = piece_parent_data.get("parent_value")
            parent_side = piece_parent_data.get("parent_side")
            parent_row_index = piece_parent_data.get("parent_row_index")
            parent_sticker_index = piece_parent_data.get("parent_sticker_index")

            to_side_mappings = {
                cube_client.front_side[1][1]: "front_side",
                cube_client.back_side[1][1]: "back_side",
                cube_client.left_side[1][1]: "left_side",
                cube_client.right_side[1][1]: "right_side"
            } 
            from_to_move_config = {
                ('back_side', 2, 1, 'left_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'down', 1), ('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('rotate_cube', 'left', 2), ('move_cube', 'top', 'horizontal', 'left', 2)],
                ('bottom_side', 0, 1, 'back_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'left', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('bottom_side', 0, 1, 'front_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 2), ('rotate_cube', 'left', 1)],
                ('bottom_side', 0, 1, 'left_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 2)],
                ('bottom_side', 0, 1, 'right_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 2)],
                ('bottom_side', 1, 0, 'back_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('bottom_side', 1, 0, 'front_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'right', 1)],
                ('bottom_side', 1, 0, 'left_side', 'top_side'): [('move_cube', 'left', 'vertical', 'up', 2)],
                ('bottom_side', 1, 0, 'right_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 2)],
                ('bottom_side', 1, 2, 'back_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'right', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'right', 1)],
                ('bottom_side', 1, 2, 'front_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('bottom_side', 1, 2, 'left_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 2), ('move_cube', 'left', 'vertical', 'up', 2)],
                ('bottom_side', 1, 2, 'right_side', 'top_side'): [('move_cube', 'right', 'vertical', 'up', 2)],
                ('bottom_side', 2, 1, 'back_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 2), ('rotate_cube', 'left', 1)],
                ('bottom_side', 2, 1, 'front_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'left', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 2), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('bottom_side', 2, 1, 'left_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 1), ('move_cube', 'left', 'vertical', 'up', 2)],
                ('bottom_side', 2, 1, 'right_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 2)],
                ('front_side', 2, 1, 'front_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'down', 1), ('rotate_cube', 'left', 1)],
                ('front_side', 2, 1, 'left_side', 'top_side'): [('rotate_cube', 'right', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('rotate_cube', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1)],
                ('left_side', 2, 1, 'front_side', 'top_side'): [('move_cube', 'top', 'horizontal', 'left', 1), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('rotate_cube', 'left', 1)],
                ('left_side', 2, 1, 'left_side', 'top_side'): [('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('rotate_cube', 'left', 1), ('move_cube', 'top', 'horizontal', 'left', 1)],
                ('left_side', 2, 1, 'right_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'left', 2), ('move_cube', 'right', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'left', 1), ('rotate_cube', 'left', 1), ('move_cube', 'right', 'vertical', 'down', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'right', 1)],
                ('right_side', 2, 1, 'left_side', 'top_side'): [('move_cube', 'bottom', 'horizontal', 'right', 2), ('move_cube', 'left', 'vertical', 'up', 1), ('move_cube', 'top', 'horizontal', 'right', 1), ('rotate_cube', 'right', 1), ('move_cube', 'right', 'vertical', 'up', 1), ('rotate_cube', 'left', 1), ('move_cube', 'top', 'horizontal', 'left', 1)],
            }
            destination_side = "top_side"
            move_from_to = ( parent_side, parent_row_index, parent_sticker_index, to_side_mappings[ piece_color ], destination_side )
            print( move_from_to )

            if move_from_to not in from_to_move_config:
                details = f"Sorting top cross piece is not supported! - {move_from_to}"
                print( details )
                cube_client.visualize_cube()
                raise Exception( details )
            
            required_moves = from_to_move_config[ move_from_to ]

            for move in required_moves:
                print( move )
                if move[0] == "rotate_cube":
                    _, direction, turns = move
                    cube_client.rotate_cube( direction, turns )
                    steps_to_solve.append( ["rotate_cube", direction, turns] )

                elif move[0] == "move_cube": 
                    _, section, orientation, direction, turns = move
                    cube_client.move_cube( section, orientation, direction, turns )
                    steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )
            continue

        else:
            break
            # cube_client.visualize_cube()
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
    cube_client.visualize_cube()
    return step_1_status, steps_to_solve