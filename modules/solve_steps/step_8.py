
# STEP 8

# LOG_STEP_INFO = True
LOG_STEP_INFO = False

def solve_cube__step_8( cube_client, test_id=None ):
	"""
    This function should output a list of moves to solve the final corner bricks. 
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

    DESCRIPTION:
		if any corners are in the correct spot, start by rotating the cube to the right, if the next piece is solved keep rotating it to the right so you start with an unsolved corner.
		once the unsolved corner is in place, repeat these steps until the corner is solved!:
			- right up
			- top left
			- right down
			- top left
		once corner is its solved:
			- rotate bottom to right
			- repeat steps above
		once all the corners are solved, it should only require rotating the bottom to get a perfect cube!!
    """

	# print( f"STEP 8 TEST {cube_client.print_json_cube()}" )
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 8!" )

	step_errors = []

	def refresh_data():
		
		pieces_to_fix = []
		indexes_to_fix = {
			# top side indexes
			( "bottom_side", 0, 0 ): False,
			( "bottom_side", 0, 2 ): False,
			( "bottom_side", 2, 2 ): False,
			( "bottom_side", 2, 0 ): False,
		}

		for index_to_fix in indexes_to_fix:

			raw_brick_data = cube_client.read_brick( *index_to_fix )
			brick_data = raw_brick_data[0]

			all_sides = list( brick_data.keys() )
			all_sides.remove( "parent_data" )

			# top_side color
			parent_data = brick_data.get("parent_data")
			matches_side = parent_data.get("matches_side")

			brick_color_values = []
			brick_color_values.append( matches_side )

			for related_side in all_sides:
				related_data = brick_data[related_side]
				related_side_matches = related_data.get( "matches_side" )
				brick_color_values.append( related_side_matches )

			if brick_color_values.count( True ) == 3:
				indexes_to_fix[index_to_fix] = True
			else:
				pieces_to_fix.append( brick_data )

		return pieces_to_fix, indexes_to_fix


	game_loop_max_count = 20
	# game_loop_max_count = 3
	game_loop_iteration = 0
	game_loop_complete = False
	cube_solved = False

	given_front_side_color = cube_client["front_side"][1][1]
	given_left_side_color = cube_client["left_side"][1][1]

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

		if cube_solved == True:
			print( "Step 8 - Final corners in place, CUBE IS SOLVED!!!!!!" ) 
			cube_client.visualize_cube()
			step_status = "PASS"
			break


		pieces_to_fix, indexes_to_fix = refresh_data()

		# if LOG_STEP_INFO == True:
		# 	print( f"pieces_to_fix: {pieces_to_fix}" )
		# 	print( f"indexes_to_fix: {indexes_to_fix}" )

		required_moves = []

		# 1. only for 1st iteration, rotate cube where the first solved piece is in the front right corner
		if game_loop_iteration == 1 and cube_solved == False:
			
			index_iteration_order = [
				('bottom_side', 0, 2),
				('bottom_side', 0, 0),
				('bottom_side', 2, 0),
				('bottom_side', 2, 2)
			]

			for i in range( len( index_iteration_order ) ):
				index = index_iteration_order[i]
				piece_is_perfect = indexes_to_fix[index]

				if LOG_STEP_INFO == True:
					print( piece_is_perfect )

				if piece_is_perfect:
					if i != 0:
						required_moves = [ ( "rotate_cube", "right", i ) ]

		front_row_is_perfect = cube_client["front_side"][2][0] == cube_client["front_side"][2][1] == cube_client["front_side"][2][2]
		right_row_is_perfect = cube_client["right_side"][2][0] == cube_client["right_side"][2][1] == cube_client["right_side"][2][2]
		back_row_is_perfect = cube_client["back_side"][2][0] == cube_client["back_side"][2][1] == cube_client["back_side"][2][2]
		left_row_is_perfect = cube_client["left_side"][2][0] == cube_client["left_side"][2][1] == cube_client["left_side"][2][2]

		bottom_row_is_perfect = [ front_row_is_perfect, right_row_is_perfect, back_row_is_perfect, left_row_is_perfect ]

		# 2. if its not perfect repeat special move until all corners are perfect, then return the PERFECT CUBE
		if bottom_row_is_perfect.count( False ) == 0 and cube_solved == False:

			# if it hits this, all bricks on the bottom row should be in perfect condition
			if LOG_STEP_INFO == True:
				print( "CUBE IS PERFECT BUT MAY NEED SHIFTING" )
			front_color = cube_client["front_side"][1][1]

			current_side_color_mappings = {
				cube_client["front_side"][2][1]: "front_side",
				cube_client["left_side"][2][1]: "left_side",
				cube_client["back_side"][2][1]: "back_side",
				cube_client["right_side"][2][1]: "right_side",
				cube_client["top_side"][2][1]: "top_side",
				cube_client["bottom_side"][2][1]: "bottom_side",
			}

			# what side needs to move to the front?
			identified_side = current_side_color_mappings[ front_color ]

			if LOG_STEP_INFO == True:
				print( f"move: {identified_side} -> front_side" )

			moves_config = {
				"left_side": [ ( "move_cube", "bottom", "horizontal", "right", 1 ) ],
				"back_side": [ ( "move_cube", "bottom", "horizontal", "right", 2 ) ],
				"right_side": [ ( "move_cube", "bottom", "horizontal", "left", 1 ) ],
			}


			if identified_side != "front_side":
				required_moves = moves_config[ identified_side ]
				cube_solved = True

			# turn cube back to given state
			# cube_client.visualize_cube()
			# print( f"given_front_side_color: {given_front_side_color}" )
			if front_color != given_front_side_color:

				rotate_moves_config = {
					"left_side": ( "rotate_cube", "right", 1 ),
					"back_side": ( "rotate_cube", "right", 2 ),
					"right_side": ( "rotate_cube", "left", 1 ),
					"top_side": ( "rotate_cube", "down", 1 ),
					"bottom_side": ( "rotate_cube", "up", 1 ),
					"front_side": ( "rotate_cube", "up", 0 ),
				}

				mapped_side = current_side_color_mappings[ given_front_side_color ]
				revert_spins_moves = rotate_moves_config[ mapped_side ]
				required_moves.append( revert_spins_moves )

				mapped_side = current_side_color_mappings[ given_left_side_color ]
				revert_spins_moves = rotate_moves_config[ mapped_side ]
				required_moves.append( revert_spins_moves )



		# 3. if front right corner piece is perfect rotate cube to the right
		if len( required_moves ) == 0 and cube_solved == False:

			# front_right_piece_coords = ('bottom_side', 0, 2)
			# front_right_piece_data = cube_client.read_brick( *front_right_piece_coords )

			front_side_color = cube_client["front_side"][2][1]
			right_side_color = cube_client["right_side"][2][1]
			bottom_side_color = cube_client["bottom_side"][1][1]

			compare__front_side_color = cube_client["front_side"][2][2]
			compare__right_side_color = cube_client["right_side"][2][0]
			compare__bottom_side_color = cube_client["bottom_side"][0][2]

			front_compare_is_perfect = front_side_color == compare__front_side_color
			right_compare_is_perfect = right_side_color == compare__right_side_color
			bottom_compare_is_perfect = bottom_side_color == compare__bottom_side_color

			compare_brick_is_perfect = [ front_compare_is_perfect, right_compare_is_perfect, bottom_compare_is_perfect ]

			if LOG_STEP_INFO == True:
				print( f"compare_brick_is_perfect: {compare_brick_is_perfect}" )

			if (
				compare_brick_is_perfect.count( False ) == 0
			):
				required_moves = [ ( "move_cube", "bottom", "horizontal", "right", 1 ) ]

		if len( required_moves ) == 0 and cube_solved == False:
			if LOG_STEP_INFO == True:
				print( indexes_to_fix )

			shift_piece_move = [
				# - right up
				# - top left
				# - right down
				# - top right
				( "move_cube", "right", "vertical", "up", 1 ),
				( "move_cube", "top", "horizontal", "left", 1 ),
				( "move_cube", "right", "vertical", "down", 1 ),
				( "move_cube", "top", "horizontal", "right", 1 ),
			]
			required_moves = shift_piece_move

		if not len( required_moves ):
			cube_solved = True

		for move in required_moves:
			if LOG_STEP_INFO == True:
				print( move )
			if move[0] == "rotate_cube":
				_, direction, turns = move
				cube_client.rotate_cube( direction, turns )
				steps_to_solve.append( ["rotate_cube", direction, turns] )

			elif move[0] == "move_cube": 
				_, section, orientation, direction, turns = move
				cube_client.move_cube( section, orientation, direction, turns )
				steps_to_solve.append( ["move_cube", section, orientation, direction, turns] )


		# ... step logic
		# step_errors.append( "STEP NOT IMPLEMENTED" )

	if len( step_errors ):
		print( f" \n \033[91m Errors in step 8: {step_errors} \033[0m \n" )
		raise Exception( f"Errors in step 8: {step_errors}" )
	# else:
		# step_status = True
	# 	print(  indexes_to_fix )
	# 	# print( [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ] )
	# 	print( [ is_perfect for is_perfect in indexes_to_fix.values() ] )
	# 	step_status = "PASS" if False not in [ is_perfect for is_perfect in indexes_to_fix.values() ] else "FAIL"

	return step_status, steps_to_solve