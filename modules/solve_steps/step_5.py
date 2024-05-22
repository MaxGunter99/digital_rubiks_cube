
# STEP 5

# LOG_STEP_INFO = True
LOG_STEP_INFO = False

def solve_cube__step_5( cube_client, test_id=None ):
	"""
	OVERVIEW: 
		pt 1: Get all the top cross colors in a cross, they do not have to match, just need to be on top
		pt 2: sort top cross colors to match sides

	DETAILS:
    Solve top cross ( L can match but all top should have yellow on the cross )
    we need to be able to move the cube pieces without disrupting the solved sections, this should work:
    - rotate the front to the right
    - rotate right up
    - rotate top left
    - rotate right down
    - rotate top right
    -  rotate the front to the left

    repeat steps until the top cross is solved, does not have to match sides, but try to have an L shape of matching sides
    once you have the L, match it to the sides and position it to the back and right, once this is in place follow these moves:
        - right up
        - top left
        - right down
        - top left
        - right up
        - top left 2 times
        - right down
        - top left
    Now the top cross should be solved
    """
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 5!" )

	step_errors = []

	game_loop_max_count = 20
	# game_loop_max_count = 4
	# game_loop_max_count = 2
	game_loop_iteration = 0
	game_loop_complete = False

	def refresh_data():

		pieces_to_fix = []
		# for pt 1
		indexes_matches_top_color = {
            # side, row, index: is_perfect
            ( "top_side", 0, 1 ): False,
            ( "top_side", 1, 0 ): False,
            ( "top_side", 1, 2 ): False,
            ( "top_side", 2, 1 ): False,
        }
		# for pt 2
		indexes_to_fix = {
            # side, row, index: is_perfect
            ( "top_side", 0, 1 ): False,
            ( "top_side", 1, 0 ): False,
            ( "top_side", 1, 2 ): False,
            ( "top_side", 2, 1 ): False,
        }

		index_relationships = {
			tuple( sorted( ( cube_client["top_side"][1][1], cube_client["front_side"][1][1] ) ) ): ( "top_side", 2, 1 ),
			tuple( sorted( ( cube_client["top_side"][1][1], cube_client["left_side"][1][1] ) ) ): ( "top_side", 1, 0 ),
			tuple( sorted( ( cube_client["top_side"][1][1], cube_client["back_side"][1][1] ) ) ): ( "top_side", 0, 1 ),
			tuple( sorted( ( cube_client["top_side"][1][1], cube_client["right_side"][1][1] ) ) ): ( "top_side", 1, 2 ),
		}

		top_side_color = cube_client["top_side"][1][1]
		# print( top_side_color )

		all_color_locations = cube_client.check_sides( top_side_color )
		all_side_names = list( all_color_locations.keys() )
		all_side_names.remove("best_side_data")


		# Marking pt 1
		for index_info in indexes_matches_top_color:
			side_name, row_index, sticker_index = index_info
			index_data = cube_client[side_name][row_index][sticker_index]
			if index_data == top_side_color:
				indexes_matches_top_color[index_info] = True

		if LOG_STEP_INFO == True:
			print( f"indexes_matches_top_color: {indexes_matches_top_color}" )

		# Marking pt 2
		all_side_data = []
		for side_name in all_side_names:
			pieces = all_color_locations[side_name].get("brick_data")
			all_side_data = all_side_data + pieces

		for piece in all_side_data:

			if len( piece.keys() ) != 2:
				continue

			if LOG_STEP_INFO == True:
				print( piece )

			parent_data = piece.get("parent_data")
			# parent_side = parent_data.get("parent_side")
			# parent_row_index = parent_data.get("parent_row_index")
			# parent_sticker_index = parent_data.get("parent_sticker_index")
			parent_matches_side = parent_data.get("matches_side")
			parent_value = parent_data.get("parent_value")

			related_side_name = list( piece.keys() )
			related_side_name.remove( "parent_data" )
			related_side_name = related_side_name[0]
			related_data = piece.get( related_side_name )
			# related_piece_row_index = related_data.get("row_index")
			related_piece_value = related_data.get("value")
			related_piece_matches_side = related_data.get("matches_side")

			color_search = tuple( sorted( ( parent_value, related_piece_value ) ) )
			required_coords = index_relationships[color_search]

			if required_coords in indexes_to_fix:
				piece_is_perfect = parent_matches_side == related_piece_matches_side == True
				if LOG_STEP_INFO == True:
					print( f"piece_is_perfect: {piece_is_perfect}" )

				if piece_is_perfect == False:
					pieces_to_fix.append( piece )
				indexes_to_fix[required_coords] = piece_is_perfect

		if LOG_STEP_INFO == True:
			print( f"indexes_to_fix: {indexes_to_fix}" )

		return pieces_to_fix, indexes_matches_top_color, indexes_to_fix

	while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ): 
		game_loop_iteration += 1
		if LOG_STEP_INFO == True:
			print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
			cube_client.visualize_cube()

		if game_loop_iteration >= game_loop_max_count or step_errors:
			break
		
		pieces_to_fix, indexes_matches_top_color, indexes_to_fix = refresh_data()

		# ... step logic
		# step_errors.append("STEP NOT IMPLEMENTED")
		# raise Exception( "STEP NOT IMPLEMENTED" )

		# step 1:
		step_1_list = indexes_matches_top_color.values() if len( indexes_matches_top_color ) else []
		step_1_status_values = [ i for i in step_1_list ]
		step_1_status = "PASS" if False not in step_1_status_values else "FAIL"

		step_2_list = indexes_to_fix.values() if len( indexes_to_fix ) else []
		step_2_status_values = [ i for i in step_2_list ]
		step_2_status = "PASS" if False not in step_2_status_values else "FAIL"

		if LOG_STEP_INFO == True:
			print( f"step_1_status: {step_1_status}" )
			print( f"step_2_status: {step_2_status}" )

		if step_1_status == step_2_status == "PASS":
			print( "Step 5 IS COMPLETE" )
			if LOG_STEP_INFO == True:
				cube_client.visualize_cube()
			step_status = "PASS"
			break

		required_moves = None

		if step_1_status == "FAIL" and step_2_status == "FAIL":
			if LOG_STEP_INFO == True:
				print( "need to move colors to the top" )
				# print( pieces_to_fix )
				# print( indexes_matches_top_color )

			matches_top_color_values = tuple( indexes_matches_top_color.values() )
			required_moves_key = {

				# All Ls
				( True, True, False, False ): ( "top left", "L" ),
				( True, False, True, False ): ( "top right", "L" ),
				( False, True, False, True ): ( "bottom left", "L" ),
				( False, False, True, True ): ( "bottom right", "L" ),

				# All Is
				( True, False, False, True ): ( "vertical", "I" ),
				( False, True, True, False ): ( "horizontal", "I" ),

				# None Match
				( False, False, False, False ): ( "no top cross pieces" )

			}

			if matches_top_color_values not in required_moves_key:
				details = f"matches_top_color_values ({matches_top_color_values}) is not defined in required_moves_key"
				step_errors.append( details )

			identified_move = required_moves_key[ matches_top_color_values ]
			if LOG_STEP_INFO == True:
				print( identified_move )

			# What do you need?
			# well to start, at the very least we need to get the top L correct or any straight line
			# if theres an L theres a move to fix all corners, if its vertical what do you do?

			# what move can you use without mixing up the cube more?
			right_move = [
				('rotate_cube', 'right', 1), 
				('move_cube', 'right', 'vertical', 'up', 1), 
				('rotate_cube', 'left', 1), 
				('move_cube', 'right', 'vertical', 'up', 1), 
				('move_cube', 'top', 'horizontal', 'left', 1), 
				('move_cube', 'right', 'vertical', 'down', 1), 
				('move_cube', 'top', 'horizontal', 'right', 1), 
				('rotate_cube', 'right', 1), 
				('move_cube', 'right', 'vertical', 'down', 1), 
				('rotate_cube', 'left', 1),
			]
			left_move = [
				('rotate_cube', 'left', 1), 
				('move_cube', 'left', 'vertical', 'down', 1), 
				('rotate_cube', 'right', 1), 
				('move_cube', 'left', 'vertical', 'up', 1), 
				('move_cube', 'top', 'horizontal', 'right', 1), 
				('move_cube', 'left', 'vertical', 'down', 1), 
				('move_cube', 'top', 'horizontal', 'left', 1), 
				('rotate_cube', 'left', 1), 
				('move_cube', 'right', 'vertical', 'up', 1), 
				('rotate_cube', 'right', 1),
			]

			moves_config = {
				( "no top cross pieces" ): [
					*right_move,
					*right_move,
					('move_cube', 'top', 'horizontal', 'left', 1), 
					*right_move,
					('move_cube', 'top', 'horizontal', 'right', 1), 
				],
				('horizontal', 'I'): [
					*right_move
				],
				('vertical', 'I'): [
					('move_cube', 'top', 'horizontal', 'left', 1), 
					*right_move,
					('move_cube', 'top', 'horizontal', 'right', 1), 
				],
				('bottom left', 'L'): [
					('move_cube', 'top', 'horizontal', 'left', 1), 
					*right_move,
					*right_move,
					('move_cube', 'top', 'horizontal', 'right', 1), 
				],
				('bottom right', 'L'): [
					('move_cube', 'top', 'horizontal', 'right', 2), 
					*right_move,
					*right_move,
					('move_cube', 'top', 'horizontal', 'left', 1), 
				],
				('top left', 'L'): [
					*right_move,
					*right_move,
				],
				('top right', 'L'): [
					('move_cube', 'top', 'horizontal', 'right', 1), 
					*right_move,
					*right_move,
					('move_cube', 'top', 'horizontal', 'left', 1), 
				]
			}

			if identified_move not in moves_config:
				details = f"Part 1 identified_move not in moves_config: {identified_move}"
				step_errors.append( details )
				continue

			required_moves = moves_config[ identified_move ]

		elif step_1_status == "PASS" and step_2_status == "FAIL":

			# step_errors.append("STEP 2 NOT IMPLEMENTED")
			# Find matching sides, 2 at best, else it would be a line

			sides_color_order = [
				cube_client["front_side"][1][1],
				cube_client["left_side"][1][1],
				cube_client["back_side"][1][1],
				cube_client["right_side"][1][1],
			]
			top_color_order = [
				cube_client["front_side"][0][1],
				cube_client["left_side"][0][1],
				cube_client["back_side"][0][1],
				cube_client["right_side"][0][1],
			]
			side_names_by_index = [ "front_side", "left_side", "back_side", "right_side" ]

			colors_match_bools = [ top_color_order[i] == sides_color_order[i] for i in range( 4 ) ]
			if LOG_STEP_INFO == True:
				print( f"colors_match_bools: {colors_match_bools}" )
				print( sides_color_order )

			# What do you need to look for?

			# 1. Line up as many pieces as you can using right_move, should be all 4 or just 2

			# what do you need to call out? 
			# Matching sides, 2 or 4 should match

			align_colors_moves = []

			for side in range( len( top_color_order ) ):
				color = top_color_order[side]
				next_color = top_color_order[ side + 1 ] if side + 1 < len( top_color_order ) else top_color_order[0]

				if f"{color}{next_color}" in "".join( sides_color_order + sides_color_order ):
					color_found_origin_index = top_color_order.index( color )
					color_found_from_side_name = side_names_by_index[ color_found_origin_index ]

					color_found_destination_index = sides_color_order.index( color )
					color_found_to_side_name = side_names_by_index[ color_found_destination_index ]

					if color_found_from_side_name != color_found_to_side_name:

						if LOG_STEP_INFO == True:
							print( f"color: {color} from {color_found_from_side_name} to {color_found_to_side_name}" )
						moves_config = {
							( "front_side", "right_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 1) ],
							( "front_side", "back_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 2) ],
							( "front_side", "left_side" ): [ ('move_cube', 'top', 'horizontal', 'left', 1) ],

							( "left_side", "back_side" ): [ ('move_cube', 'top', 'horizontal', 'left', 1) ],
							( "left_side", "right_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 2) ],
							( "left_side", "front_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 1) ],
							
							( "back_side", "right_side" ): [ ('move_cube', 'top', 'horizontal', 'left', 1) ],
							( "back_side", "front_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 2) ],
							( "back_side", "left_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 1) ],

							( "right_side", "front_side" ): [ ('move_cube', 'top', 'horizontal', 'left', 1) ],
							( "right_side", "left_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 2) ],
							( "right_side", "back_side" ): [ ('move_cube', 'top', 'horizontal', 'right', 1) ],
						}

						move_from_to = ( color_found_from_side_name, color_found_to_side_name )
						align_colors_moves = moves_config[ move_from_to ]

			if align_colors_moves != []:
				if LOG_STEP_INFO == True:
					print( "lining up colors, no other required moves now" )
				required_moves = align_colors_moves

			else:

				# ...

				# 2. if L, hold them to back and right ( if across (H or V?) do this from anywhere )

				top_side_colors = [
					cube_client["front_side"][0][1],
					cube_client["left_side"][0][1],
					cube_client["back_side"][0][1],
					cube_client["right_side"][0][1],
				]
				side_colors = [
					cube_client["front_side"][1][1],
					cube_client["left_side"][1][1],
					cube_client["back_side"][1][1],
					cube_client["right_side"][1][1],
				]
				colors_matches_side_list = [ top_side_colors[i] ==  side_colors[i] for i in range( 4 ) ]

				matches_top_color_values = tuple( colors_matches_side_list )
				required_moves_key = {

					# All Ls
					( False, True, True, False ): ( "top left", "L" ),
					( False, False, True, True ): ( "top right", "L" ),
					( True, True, False, False ): ( "bottom left", "L" ),
					( True, False, False, True ): ( "bottom right", "L" ),

					# All Is
					( True, False, True, False ): ( "vertical", "I" ),
					( False, True, False, True ): ( "horizontal", "I" ),

					# None Match
					( False, False, False, False ): ( "no top cross pieces" )

				}

				identified_move = required_moves_key[matches_top_color_values]
				if LOG_STEP_INFO == True:
					print( f"identified_move to fix colors post alignment: {identified_move}" )

				fix_L_move = {
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'top', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'top', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'top', 'horizontal', 'right', 2),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'top', 'horizontal', 'left', 1),
				}

				moves_config_pt_2 = {
					( "no top cross pieces" ): [
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
					],
					('horizontal', 'I'): [
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
					],
					('vertical', 'I'): [
						('rotate_cube', 'left', 1), 
						# *fix_L_move ,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),

						('rotate_cube', 'right', 1), 
					],
					('bottom left', 'L'): [
						('rotate_cube', 'left', 2), 
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),

						('rotate_cube', 'left', 2), 
					],
					('bottom right', 'L'): [
						('rotate_cube', 'right', 1), 
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),

						('rotate_cube', 'left', 1), 
					],
					('top left', 'L'): [
						('rotate_cube', 'left', 1), 
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),

						('rotate_cube', 'right', 1), 
					],
					('top right', 'L'): [
						# *fix_L_move,
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
						('move_cube', 'right', 'vertical', 'up', 1),
						('move_cube', 'top', 'horizontal', 'right', 2),
						('move_cube', 'right', 'vertical', 'down', 1),
						('move_cube', 'top', 'horizontal', 'left', 1),
					]
				}

				if identified_move not in moves_config_pt_2:
					details = f"Error in part 2, identified_move: {identified_move} not in moves config"
					print( details )
					step_errors.append( details )
					break

				required_moves = moves_config_pt_2[identified_move]
				if LOG_STEP_INFO == True:
					print( f"Moves to to fix all top side colors: {required_moves}" )




		if LOG_STEP_INFO == True:
			cube_client.visualize_cube()
			print( "BEFORE MOVE" )

		# required_moves = left_move

		if not required_moves:
			print( "Required moves are empty, breaking" )
			break


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

		if LOG_STEP_INFO == True:
			cube_client.visualize_cube()
			print( "AFTER MOVE" )



	if len( step_errors ):
		print( f" \n \033[91m Errors in step 5: {step_errors} \033[0m \n" )
		raise Exception( f"Errors in step 5: {step_errors}" )
	else:
		top_side_colors = [
			cube_client["front_side"][0][1],
			cube_client["left_side"][0][1],
			cube_client["back_side"][0][1],
			cube_client["right_side"][0][1],
		]
		side_colors = [
			cube_client["front_side"][1][1],
			cube_client["left_side"][1][1],
			cube_client["back_side"][1][1],
			cube_client["right_side"][1][1],
		]
		colors_matches_side_list = [ top_side_colors[i] ==  side_colors[i] for i in range( 4 ) ]
		if colors_matches_side_list.count(False) == 0:
			step_status = "PASS"

	return step_status, steps_to_solve