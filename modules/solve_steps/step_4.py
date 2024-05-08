
# STEP 4

LOG_STEP_INFO = True
# LOG_STEP_INFO = False

def solve_cube__step_4( cube_client, test_id=None ):
	"""
	Solve on the middle section
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

    DESCRIPTION:
		- find any mismatching piece on the top middle that should be in the middle side
		- align it to the correct side, if it needs to go the the middle right ( else do reverse ):
			- rotate top section horizontally away (left)
			- rotate vertical right up
			- rotate horizontal top left
			- rotate top section horizontally right
			- rotate cube left
			reverse moves from left side
			- rotate the left vertical side up
			- top to the horizontal right
			- left vertical side up
			- top horizontal to the left

			repeat steps until the middle is solved.

			if the piece is reversed and needs to be ejected, repeat the same process as if you are going to insert and try again.
    """
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 4!" )

	step_errors = []

	def refresh_data():

		if LOG_STEP_INFO == True:
			print( "REFRESHING DATA" )

		indexes_to_fix = {
            # side, row, index: is_perfect
            ( ( "front_side", 1, 0 ), ( "left_side", 1, 2 ) ): False,
            ( ( "left_side", 1, 0 ), ( "back_side", 1, 2 ) ): False,
            ( ( "back_side", 1, 0 ), ( "right_side", 1, 2 ) ): False,
			( ( "right_side", 1, 0 ), ( "front_side", 1, 2 ) ): False,
        }

		pieces_to_fix = []

		# 1. check these sides and coords to see if they match the given side, mark each index as is_perfect if it matches
  
		def check_coord_matches_side( side_name, row_index, sticker_index ):

			# if LOG_STEP_INFO == True:
			# 	print( f"checking coord: {side_name, row_index, sticker_index}" )

			side_color = cube_client[side_name][1][1]
			coord_value = cube_client[side_name][row_index][sticker_index]
			sticker_matches_side = side_color == coord_value
			return sticker_matches_side

		for coords_to_fix in indexes_to_fix.keys():

			coords_are_prefect = False

			coord_1 = coords_to_fix[0]
			coord_2 = coords_to_fix[1]

			if LOG_STEP_INFO == True:
				print( f"\n Checking: {coord_1} and {coord_2}" )

			coord_1_is_perfect = check_coord_matches_side( *coord_1 )
			coord_2_is_perfect = check_coord_matches_side( *coord_2 )
			coord_colors = []
			coord_colors.append( cube_client[ coord_1[0] ][1][1] )
			coord_colors.append( cube_client[ coord_2[0] ][1][1] )
			coord_colors = sorted( coord_colors )
			# print( f"coord_colors: {coord_colors}" )

			if LOG_STEP_INFO == True:
				print( f"coords is_perfect: {coord_1_is_perfect} and {coord_2_is_perfect}" )

			if coord_1_is_perfect == True and coord_2_is_perfect == True:
				coords_are_prefect = True
				indexes_to_fix[coords_to_fix] = coords_are_prefect
				continue
  
			# 2. if its not perfect find where these currently are and add them to pieces_to_fix
			if LOG_STEP_INFO == True:
				print( f"Finding location of: {coord_1} and {coord_2}" )
			
			coord_1_side_color = cube_client[coord_1[0]][1][1]
			all_color_locations = cube_client.check_sides( coord_1_side_color )
			for side_name, side_data in all_color_locations.items():

				# print( side_data.get('brick_data') )

				if side_data.get('brick_data') != None:

					for pieces in side_data.get('brick_data'):
						if len( pieces ) >= 3 or len( pieces ) == 1:
							continue
						color_1 = pieces.get( "parent_data" ).get("parent_value")
						key = [ i for i in pieces.keys() ]
						key.remove("parent_data")
						color_2 = pieces.get(key[0]).get("value")
						sorted_colors_found = sorted( [color_1, color_2] )
						if coord_colors == sorted_colors_found:
							print( f"FOUND IT" )
							print( pieces )
							pieces_to_fix.append( pieces )
  
		return ( pieces_to_fix, indexes_to_fix )

	# game_loop_max_count = 20
	game_loop_max_count = 1
	game_loop_iteration = 0
	game_loop_complete = False

	while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ):
		if LOG_STEP_INFO == True:
			print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
			cube_client.visualize_cube()

		if game_loop_iteration >= game_loop_max_count:
			break


		pieces_to_fix, indexes_to_fix_status = refresh_data()
		count_of_pieces_to_fix = len( [ v for v in indexes_to_fix_status.values() ] )
		
		if len( pieces_to_fix ) != count_of_pieces_to_fix:
			raise Exception( f"pieces_to_fix does not equal 4, we need all 4 corners" )

		print( f"pieces_to_fix: {pieces_to_fix}" ) 
		print( f"indexes_to_fix_status: {[ val for _, val in indexes_to_fix_status.items() ]}" )

		# raise Exception( "STEP NOT IMPLEMENTED" )
		game_loop_iteration += 1

	if len( step_errors ):
		print( f"Errors in step x: {step_errors}" )
		raise Exception( f"Errors in step x: {step_errors}" )

	return step_status, steps_to_solve