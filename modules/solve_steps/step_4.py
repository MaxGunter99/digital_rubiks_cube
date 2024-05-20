
# STEP 4

# LOG_STEP_INFO = True
LOG_STEP_INFO = False

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
		new_indexes_to_fix = {}
		pieces_to_fix = []

		side_name_color_mappings = {
			cube_client["front_side"][1][1]: "front_side",
			cube_client["left_side"][1][1]: "left_side",
			cube_client["right_side"][1][1]: "right_side",
			cube_client["back_side"][1][1]: "back_side",
		}

		destination_sticker_indexes = {
			# parent destination - related destination: index
			("front_side", "left_side"): 0,
			("front_side", "right_side"): 2,

			("left_side", "back_side"): 0,
			("left_side", "front_side"): 2,

			("back_side", "right_side"): 0,
			("back_side", "left_side"): 2,

			("right_side", "front_side"): 0,
			("right_side", "back_side"): 2,
		}
		return_indexes_to_fix = {}

		for coord in indexes_to_fix.keys():
			coord_1, coord_2 = coord
			coord_1_side_name, coord_1_row_number, coord_1_sticker_index = coord_1
			coord_2_side_name, coord_2_row_number, coord_2_sticker_index = coord_2

			coord_1_color = cube_client[coord_1_side_name][1][1]
			coord_2_color = cube_client[coord_2_side_name][1][1]

			new_key = tuple( sorted( [coord_1_color, coord_2_color ] ) )
			new_indexes_to_fix[ new_key ] = False

		for side_name in [ "front_side", "left_side", "back_side", "right_side" ]:
			side_color = cube_client[side_name][1][1]
			all_color_locations = cube_client.check_sides( side_color )

			if LOG_STEP_INFO == True:
				print( f"checking side: {side_color}" )
				print( all_color_locations.items() )

			sides_brick_data = [ side_data.get( "brick_data", [] ) for _, side_data in all_color_locations.items() ]
			filtered_sides_brick_data = []
			for x in sides_brick_data:
				for i in x:
					filtered_sides_brick_data.append( i )

			# print( filtered_sides_brick_data )
			for brick in filtered_sides_brick_data:

				if len( brick ) == 2:

					parent_data = brick.get("parent_data")
					parent_color = parent_data.get("parent_value")
					parent_matches_side = parent_data.get("matches_side")

					related_side_key = list( brick.keys() )
					related_side_key.remove( "parent_data" )
					related_side_color = brick[related_side_key[0]].get("value")
					related_side_matches_side = brick[related_side_key[0]].get("matches_side")

					search_key = tuple( sorted( [ parent_color, related_side_color ] ) )

					if search_key in new_indexes_to_fix:
						if LOG_STEP_INFO == True:
							print( search_key )
							print( f"\n\n brick to fix: {brick}" )
						new_side_destination = side_name_color_mappings[parent_color]
						new_row_index = 1
						related_side_destination = side_name_color_mappings[related_side_color ]
						new_sticker_index = destination_sticker_indexes[ ( new_side_destination, related_side_destination ) ]
						destination_data = ( new_side_destination, new_row_index, new_sticker_index )
						brick["fixed_coords"] = destination_data


						if parent_matches_side == True and related_side_matches_side == True:
							new_indexes_to_fix[ search_key ] = True
							return_indexes_to_fix[search_key] = True
						else:
							pieces_to_fix.append( brick )
							return_indexes_to_fix[search_key] = False

		if LOG_STEP_INFO == True:
			print( f"\n\nreturn_indexes_to_fix: {return_indexes_to_fix}" )


		return ( pieces_to_fix, return_indexes_to_fix )

	

	# VARIABLES USED IF WE REUSE MOVES
	move_extended = False
	extended_moves = []
	reverse_extended_moves = []

	game_loop_max_count = 20
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

		game_loop_iteration += 1

		pieces_to_fix, indexes_to_fix_status = refresh_data()
		is_perfect_bools = [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ]
		
		if not len( pieces_to_fix ) or is_perfect_bools.count(False) == 0:
			if LOG_STEP_INFO == True:
				print( "Step 4 pieces are perfect, on to the next" )
				cube_client.visualize_cube()
			break

		# print( f"pieces_to_fix: {pieces_to_fix}" ) 
		
		moves_do_not_need_extended_moves = []
		moves_need_extended_moves = []

		# FIX NON EXTENDED MOVES FIRST
		for to_fix in pieces_to_fix:
			requires_extended_moves = False
			parent_data = to_fix.get("parent_data", [])
			parent_side = parent_data.get( "parent_side" )
			parent_row_index = parent_data.get( "parent_row_index" )
			parent_sticker_index = parent_data.get( "parent_sticker_index" )

			if (
				parent_side == "top_side" and parent_row_index == 0
				or parent_side == "back_side"
			):
				requires_extended_moves = True

			elif (
				parent_side == "left_side"
				or parent_side == "top_side" and parent_row_index == 1 and parent_sticker_index == 0
			):
				requires_extended_moves = True

			elif (
				parent_side == "right_side"
				or parent_side == "top_side" and parent_row_index == 1 and parent_sticker_index == 2
			):
				requires_extended_moves = True

			if requires_extended_moves == True:
				moves_need_extended_moves.append( to_fix )
			else:
				moves_do_not_need_extended_moves.append( to_fix )

		sorted_pieces_to_fix = moves_do_not_need_extended_moves + moves_need_extended_moves
  
		piece_to_fix = sorted_pieces_to_fix[0]

		parent_data = piece_to_fix.get("parent_data")
		parent_side = parent_data.get("parent_side")
		parent_row_index = parent_data.get("parent_row_index")
		parent_sticker_index = parent_data.get("parent_sticker_index")
		fixed_coords = piece_to_fix.get("fixed_coords")
		is_perfect = piece_to_fix.get("brick_is_perfect")
		move_from_to = ( parent_side, parent_row_index, parent_sticker_index, fixed_coords )

		# MOVE PATTERNS TO BE REUSED
		pop_out_right = [
			('move_cube', 'right', 'vertical', 'up', 1), 
			('move_cube', 'top', 'horizontal', 'left', 1), 
			('move_cube', 'right', 'vertical', 'down', 1), 
			('move_cube', 'top', 'horizontal', 'right', 1), 
			('rotate_cube', 'left', 1),
			('move_cube', 'left', 'vertical', 'up', 1), 
			('move_cube', 'top', 'horizontal', 'right', 1), 
			('move_cube', 'left', 'vertical', 'down', 1), 
			('move_cube', 'top', 'horizontal', 'left', 1), 
			('rotate_cube', 'right', 1),
		]
		pop_out_left = [
			('move_cube', 'left', 'vertical', 'up', 1), 
			('move_cube', 'top', 'horizontal', 'right', 1), 
			('move_cube', 'left', 'vertical', 'down', 1), 
			('move_cube', 'top', 'horizontal', 'left', 1),
			('rotate_cube', 'right', 1), 
			('move_cube', 'right', 'vertical', 'up', 1), 
			('move_cube', 'top', 'horizontal', 'left', 1), 
			('move_cube', 'right', 'vertical', 'down', 1), 
			('move_cube', 'top', 'horizontal', 'right', 1), 
			('rotate_cube', 'left', 1),
		]

		moves_config = {
			('front_side', 1, 2, ('right_side', 1, 0)): [
				*pop_out_right,
				('move_cube', 'top', 'horizontal', 'left', 2), 
				*pop_out_right,
			],
			('front_side', 1, 0, ('left_side', 1, 2)): [
				*pop_out_left,
				('move_cube', 'top', 'horizontal', 'right', 2), 
				*pop_out_left
			],
			('front_side', 1, 0, ('right_side', 1, 0)): [
				('rotate_cube', 'right', 1),
				*pop_out_right,
				('rotate_cube', 'right', 2),
				('move_cube', 'top', 'horizontal', 'left', 2), 
				*pop_out_left,
				('rotate_cube', 'right', 1),
			],
			('front_side', 1, 0, ('front_side', 1, 2)): [
				*pop_out_left,
				('rotate_cube', 'left', 1),
				('move_cube', 'top', 'horizontal', 'left', 1), 
				*pop_out_left,
				('rotate_cube', 'right', 1),
			],
			('front_side', 1, 0, ('back_side', 1, 0)): [
				*pop_out_left,
				('rotate_cube', 'right', 2),
				('move_cube', 'top', 'horizontal', 'left', 2), 
				*pop_out_right,
				('rotate_cube', 'left', 2),
			],
			('front_side', 1, 0, ('back_side', 1, 2)): [
				('rotate_cube', 'right', 1),
				*pop_out_right,
				('move_cube', 'top', 'horizontal', 'right', 1), 
				('rotate_cube', 'right', 1),
				*pop_out_right,
				('rotate_cube', 'right', 2),
			],
			('front_side', 1, 0, ('left_side', 1, 0)): [
				*pop_out_left,
				('rotate_cube', 'right', 2),
				('move_cube', 'top', 'horizontal', 'left', 2), 
				*pop_out_right,
				('rotate_cube', 'left', 2),
			],
			('front_side', 1, 0, ('right_side', 1, 2)): [
				*pop_out_left,
				('rotate_cube', 'left', 2),
				*pop_out_left,
				('rotate_cube', 'right', 2),
			],
			('front_side', 1, 2, ('back_side', 1, 0)): [
				*pop_out_right,
				('move_cube', 'top', 'horizontal', 'left', 1),
				('rotate_cube', 'left', 1),
				*pop_out_right,
				('rotate_cube', 'right', 1),
			],
			('front_side', 1, 2, ('back_side', 1, 2)): [
				*pop_out_right,
				('rotate_cube', 'right', 1),
				('move_cube', 'top', 'horizontal', 'left', 1),
				*pop_out_left,
				('rotate_cube', 'left', 1),
			],
			('front_side', 1, 2, ('left_side', 1, 0)): [
				*pop_out_right,
				('rotate_cube', 'left', 2),
				*pop_out_right,
				('rotate_cube', 'right', 2),
			],
			('front_side', 0, 1, ('left_side', 1, 0)): [
				('rotate_cube', 'right', 1),
				*pop_out_left,
				('rotate_cube', 'left', 1),
			],
			('top_side', 2, 1, ('left_side', 1, 0)): [
				('rotate_cube', 'right', 2),
				('move_cube', 'top', 'horizontal', 'right', 1),
				*pop_out_right,
				('rotate_cube', 'left', 2),
			],
			('front_side', 0, 1, ('front_side', 1, 0)): [
				('move_cube', 'top', 'horizontal', 'right', 1),
				*pop_out_left,
			],
			('top_side', 2, 1, ('front_side', 1, 0)): [
				('rotate_cube', 'right', 1),
				('move_cube', 'top', 'horizontal', 'left', 2),
				*pop_out_right,
				('rotate_cube', 'left', 1),
			],
			('front_side', 0, 1, ('back_side', 1, 0)): [
				('rotate_cube', 'left', 2),
				('move_cube', 'top', 'horizontal', 'left', 1),
				*pop_out_left,
				('rotate_cube', 'right', 2),
			],
			('top_side', 2, 1, ('back_side', 1, 0)): [
				('rotate_cube', 'left', 1),
				*pop_out_right,
				('rotate_cube', 'right', 1),
			],
			('top_side', 2, 1, ('front_side', 1, 2)): [
				('rotate_cube', 'left', 1),
				('move_cube', 'top', 'horizontal', 'right', 2),
				*pop_out_left,
				('rotate_cube', 'right', 1),
			],
			('front_side', 0, 1, ('front_side', 1, 2)): [
				('move_cube', 'top', 'horizontal', 'left', 1),
				*pop_out_right,
			],
			('front_side', 1, 2, ('front_side', 1, 0)): [
				*pop_out_right,
				('rotate_cube', 'right', 1),
				('move_cube', 'top', 'horizontal', 'right', 1),
				*pop_out_right,
				('rotate_cube', 'left', 1),
			],
			('front_side', 1, 2, ('right_side', 1, 2)): [
				*pop_out_right,
				('rotate_cube', 'left', 2),
				('move_cube', 'top', 'horizontal', 'right', 2),
				*pop_out_left,
				('rotate_cube', 'right', 2),
			],
			('front_side', 1, 2, ('left_side', 1, 2)): [
				*pop_out_right,
				*pop_out_left,
			]
		}

		if LOG_STEP_INFO == True:
			print( f"move_from_to used: {move_from_to}" )

		if move_from_to not in moves_config.keys():
			use_extended_move = False

			if (
				parent_side == "top_side" and parent_row_index == 0
				or parent_side == "back_side"
			):
				use_extended_move = True
				extended_moves = [('rotate_cube', 'right', 2)]
				reverse_extended_moves = [('rotate_cube', 'right', 2)]

			elif (
				parent_side == "left_side"
				or parent_side == "top_side" and parent_row_index == 1 and parent_sticker_index == 0
			):
				use_extended_move = True
				extended_moves = [('rotate_cube', 'right', 1)]
				reverse_extended_moves = [('rotate_cube', 'left', 1)]

			elif (
				parent_side == "right_side"
				or parent_side == "top_side" and parent_row_index == 1 and parent_sticker_index == 2
			):
				use_extended_move = True
				extended_moves = [('rotate_cube', 'left', 1)]
				reverse_extended_moves = [('rotate_cube', 'right', 1)]

			if use_extended_move:
				if LOG_STEP_INFO == True:
					print(f"APPLYING EXTENDED MOVE - {extended_moves}")
				move_extended = True
				for move in extended_moves:
					_, direction, turns = move
					cube_client.rotate_cube( direction, turns )
					steps_to_solve.append( ["rotate_cube", direction, turns] )
				continue

			# TODO: needs pre / post turning for specific moves
			details = f"Fix not implemented for move - {move_from_to}"
			step_errors.append( details )
			break

		required_moves = moves_config[move_from_to]

		if required_moves == None:
			details = f"required_moves is not configured yet: {move_from_to} - is None"
			step_errors.append( details )
			break

		# REVERSE EXTENDED MOVES DATA
		if move_extended == True:
			if LOG_STEP_INFO:
				print( f"REVERSING EXTENDED MOVE - {reverse_extended_moves}")
			required_moves = required_moves + reverse_extended_moves
			move_extended = False
			extended_moves = []
			reverse_extended_moves = []

		# APPLY MOVES
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

			continue

	if len( step_errors ):
		print( f" \n \033[91m Errors in step 4: {step_errors} \033[0m \n" )
		raise Exception( f"Errors in step x: {step_errors}" )
	else:
		if LOG_STEP_INFO == True:
			print( [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ] )
		step_status = "PASS" if False not in [ is_perfect for _, is_perfect in indexes_to_fix_status.items() ] else "FAIL"

	return step_status, steps_to_solve