
# STEP 2

LOG_STEP_INFO = False

def solve_cube__step_2( cube_client, test_id=None ):
	"""
    This function should output a list of moves to solve the top cross of the cube. 
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

    DESCRIPTION:
        Solve the corners
			- find corners on outer top sides left, right, front, back.
			- match the side color.
			- turn the bottom side horizontally away
			- turn vertical color side towards white piece
			- reverse bottom horizontal turn

			If there are no outer sides left but the top is not solved, check bottom and top
			- align the mismatched pieces horizontally on top of each other, rotate them down and spin the bottom horizontally twice moving the white pieces should be on the outer sides. 
			- Repeat first 5 steps from this section
    """
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 2!" )

	step_errors = []

	game_loop_max_count = 20
	game_loop_iteration = 0
	game_loop_complete = False

	# we need to find the top corner pieces to check if they are perfect
	def refresh_data():

		if LOG_STEP_INFO == True:
			print( "REFRESHING DATA" )
		top_indexes_to_fix = {
            # row, index: is_perfect
            ( 0, 0 ): False,
            ( 0, 2 ): False,
            ( 2, 0 ): False,
            ( 2, 2 ): False
        }
		top_color_value = cube_client.top_side[1][1]
		top_color_locations = cube_client.check_sides( top_color_value )
		top_row_pieces = []
		bottom_row_pieces = []

		for side_name, side_data in top_color_locations.items():
			brick_data = side_data.get( "brick_data", [] )
			parent_locations = []

			for brick in brick_data:
				parent_data = brick.get( "parent_data" )
				parent_color = parent_data.get( "parent_value" )
				parent_row_index = parent_data.get( "parent_row_index" )
				if parent_color == top_color_value and len( brick.keys() ) == 3:

					if side_name == "top_side" or side_name in [ "front_side", "left_side", "right_side", "back_side" ] and parent_row_index == 0:
						top_row_pieces.append( brick )

					elif side_name == "bottom_side" or side_name in [ "front_side", "left_side", "right_side", "back_side" ] and parent_row_index == 2:
						bottom_row_pieces.append( brick )

		return top_row_pieces, bottom_row_pieces

	while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ): 
		game_loop_iteration += 1
		if LOG_STEP_INFO == True:
			print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
			cube_client.visualize_cube()

		if game_loop_iteration >= game_loop_max_count:
			break

		top_row_pieces, bottom_row_pieces = refresh_data()
		if 3 >= len( top_row_pieces + bottom_row_pieces ) > 4:
			raise Exception( f"Error in step 2: refresh_data function did not not find corner pieces, returned {len( top_row_pieces + bottom_row_pieces )} but should be 4" )
		
		print( f"top_row_pieces: {top_row_pieces}" )
		print( f"bottom_row_pieces: {bottom_row_pieces}" )

		print( f"top_row_pieces: {len( top_row_pieces + bottom_row_pieces )}" )
		raise Exception( "STEP NOT IMPLEMENTED" )

	if len( step_errors ):
		print( f"Errors in step 2: {step_errors}" )
		raise Exception( f"Errors in step 2: {step_errors}" )

	return step_status, steps_to_solve