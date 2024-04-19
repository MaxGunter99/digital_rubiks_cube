
# STEP 2

LOG_STEP_INFO = False

def solve_cube__step_2( cube_client, test_id=None ):
	"""
    This function should output a list of moves to solve the top corners of the cube. 
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

	game_loop_max_count = 2
	game_loop_iteration = 0
	game_loop_complete = False

	# we need to find the top corner pieces to check if they are perfect
	def refresh_data():

		if LOG_STEP_INFO == True:
			print( "REFRESHING DATA" )

		# this is all possible indexes to fix, we just need to report the ones caught
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

		fixable_piece_status = {}

		for fixable_block in top_row_pieces + bottom_row_pieces:
			# print( f"fixable_block: {fixable_block}" )

			# which of these indexes does the fixable block need to be
			grab_colors = {
				( 0, 0 ): ["left_side", "back_side"],
				( 0, 2 ): ["back_side", "right_side"],
				( 2, 0 ): ["left_side", "front_side"],
				( 2, 2 ): ["front_side", "right_side"],
			}

			for indexes in grab_colors.keys():
				required_colors = sorted([ cube_client[side_name][1][1] for side_name in grab_colors[indexes] ])
				grab_colors[indexes] = required_colors

			# collect all color values from the top side indexes and match them
			bricks_parent_data = fixable_block["parent_data"]
			bricks_parent_row = bricks_parent_data.get("parent_row_index")
			bricks_parent_sticker = bricks_parent_data.get("parent_sticker_index")
			parent_side = bricks_parent_data.get("parent_side")

			related_values = list( fixable_block.keys() )
			if "parent_data" in related_values:
				related_values.remove("parent_data")

			
			required_values = sorted( [ fixable_block[key].get("value") for key in related_values] )
			grab_colors_key = None

			if required_values in list( grab_colors.values() ):
				for key, value_list in grab_colors.items():
					if required_values == value_list:
						grab_colors_key = key

			brick_is_perfect = False

			if (
				parent_side == "top_side" 
				and grab_colors_key is not None 
				and (bricks_parent_row, bricks_parent_sticker) == grab_colors_key
			):
				brick_is_perfect = True
			fixable_piece_status[ grab_colors_key ] = brick_is_perfect

		return ( top_row_pieces, bottom_row_pieces, fixable_piece_status )

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

		top_row_pieces, bottom_row_pieces, fixable_piece_status = refresh_data()

		game_loop_complete_check = [ is_perfect for _, is_perfect in fixable_piece_status.items() ]
		if False not in game_loop_complete_check:
			if LOG_STEP_INFO == True:
				print("TOP CORNERS COMPLETE")
				game_loop_complete = True
			break
	
		if len( top_row_pieces + bottom_row_pieces ) > 4:
			raise Exception( f"Error in step 2: refresh_data function did not not find corner pieces, returned {len( top_row_pieces + bottom_row_pieces )} but should be 4" )
		
		# print( f"top_row_pieces: {top_row_pieces}" )
		# print( f"bottom_row_pieces: {bottom_row_pieces}" )

		# print( f"top_row_pieces: {len( top_row_pieces + bottom_row_pieces )}" )
  
		to_side_mappings = {
			cube_client.front_side[1][1]: "front_side",
			cube_client.back_side[1][1]: "back_side",
			cube_client.left_side[1][1]: "left_side",
			cube_client.right_side[1][1]: "right_side"
		}

	if len( step_errors ):
		print( f"Errors in step 2: {step_errors}" )
		raise Exception( f"Errors in step 2: {step_errors}" )
	else:
		step_status = "PASS" if False not in [ is_perfect for _, is_perfect in fixable_piece_status.items() ] else "FAIL"

	return step_status, steps_to_solve