
# STEP 6

LOG_STEP_INFO = False

def solve_cube__step_6( cube_client, test_id=None ):
	"""
    This function should output a list of moves to get the last corners in place. 
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

     DESCRIPTION:
	 	Corner placement, make sure the corners are in their place, does not have to be solved
		check each corner, if it is in the correct position start with that on the front right and repeat these moves until the top corners are in the correct spots, does not have to be solved, just placement
			- top left
			- right up
			- top right
			- left up
			- top left
			- right down
			- top right
			- left down
		if non corners were matching, they should have moved, check to see any matching and move it to the right.
		- repeat steps until corners are placed correctly
    """
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 6!" )

	step_errors = []

	def refresh_data():
		# grab the corner data that needs to be fixed
		# meaning it should only be corners that need to be fixed

		pieces_to_fix = []
		indexes_to_fix = {
			# top side indexes
			( "top_side", 0, 0 ): False,
			( "top_side", 0, 2 ): False,
			( "top_side", 2, 0 ): False,
			( "top_side", 2, 2 ): False,
		}

		print( sorted([ "top_side", "back_side", "left_side" ]) )
		brick_in_place_reference = {
			tuple( sorted([ "top_side", "back_side", "left_side" ]) ): sorted([	
				cube_client["top_side"][1][1],
				cube_client["back_side"][1][1],
				cube_client["left_side"][1][1],
			]),
			tuple( sorted([ "top_side", "back_side", "right_side" ]) ): sorted([ 
				cube_client["top_side"][1][1],
				cube_client["back_side"][1][1],
				cube_client["right_side"][1][1],
			]),
			tuple( sorted([ "top_side", "front_side", "left_side" ]) ): sorted([ 
				cube_client["top_side"][1][1],
				cube_client["front_side"][1][1],
				cube_client["left_side"][1][1],
			]),
			tuple( sorted([ "top_side", "front_side", "right_side" ]) ): sorted([ 
				cube_client["top_side"][1][1],
				cube_client["front_side"][1][1],
				cube_client["right_side"][1][1],
			])
		}

		for index_to_fix in indexes_to_fix:

			raw_brick_data = cube_client.read_brick( *index_to_fix )
			brick_data = raw_brick_data[0]

			all_sides = list( brick_data.keys() )
			all_sides.remove( "parent_data" )

			# print( brick_data )

			# top_side color
			parent_data = brick_data.get("parent_data")
			parent_side = parent_data.get("parent_side")
			parent_value = parent_data.get("parent_value")

			brick_color_values = []
			brick_color_values.append( parent_value )

			for related_side in all_sides:
				side_data = brick_data.get( related_side )
				side_value = side_data.get("value")
				brick_color_values.append( side_value )

			all_sides.append( parent_side )

			all_sides = sorted( all_sides )
			brick_color_values = sorted( brick_color_values )

			required_colors = brick_in_place_reference[ tuple( all_sides ) ]
			brick_is_perfect = True if required_colors == brick_color_values else False
			indexes_to_fix[ index_to_fix ] = brick_is_perfect
			if not brick_is_perfect:
				pieces_to_fix.append( brick_data )

		return pieces_to_fix, indexes_to_fix

	game_loop_max_count = 20
	game_loop_iteration = 0
	game_loop_complete = False

	while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ): 
		game_loop_iteration += 1
		if LOG_STEP_INFO == True:
			print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
			cube_client.visualize_cube()

		if game_loop_iteration >= game_loop_max_count or len( step_errors ) > 0:
			break

		pieces_to_fix, indexes_to_fix = refresh_data()

		print( f"\nindexes_to_fix: {indexes_to_fix}" )
		# print( f"pieces_to_fix: {pieces_to_fix}" )

		step_errors.append( "STEP NOT IMPLEMENTED" )


	if len( step_errors ):
		print( f" \n \033[91m Errors in step 6: {step_errors} \033[0m \n" )
		raise Exception( f"Errors in step 6: {step_errors}" )
	# else:
	# 	print( [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ] )
	# 	step_status = "PASS" if False not in [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ] else "FAIL"

	return step_status, steps_to_solve