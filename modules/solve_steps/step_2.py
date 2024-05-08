
# STEP 2

# LOG_STEP_INFO = True
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
		cube_client.print_json_cube()

	step_errors = []

	game_loop_max_count = 20
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

			# print( f"grab_colors: {grab_colors}" )
			# print( f"related_values: {related_values}" )
			
			required_values = sorted( [ fixable_block[key].get("value") for key in related_values] )
			grab_colors_key = None

			# print( f"required_values: {required_values}" )

			if required_values in list( grab_colors.values() ):
				for key, value_list in grab_colors.items():
					if required_values == value_list:
						grab_colors_key = key

			brick_is_perfect = False

			# print( ( bricks_parent_row, bricks_parent_sticker), parent_side )
			# print( f"grab_colors_key: {grab_colors_key}" )

			if (
				parent_side == "top_side" 
				and grab_colors_key is not None 
				and (bricks_parent_row, bricks_parent_sticker) == grab_colors_key
			):
				brick_is_perfect = True
			fixable_piece_status[ grab_colors_key ] = brick_is_perfect

			# assign pieces perfect location
			try:
				which_list = top_row_pieces if fixable_block in top_row_pieces else bottom_row_pieces
				which_index = which_list.index( fixable_block )
				which_list[which_index]["fixed_coords"] = grab_colors_key
				which_list[which_index]["brick_is_perfect"] = brick_is_perfect
			except ValueError:
				raise Exception( f"Error finding new location for fixable_block: {fixable_block}" )

		return ( top_row_pieces, bottom_row_pieces, fixable_piece_status )
	
	# VARIABLES USED IF WE REUSE MOVES
	move_extended = False
	extended_moves = []
	reverse_extended_moves = []

	while (
        game_loop_max_count < 10 
        or game_loop_complete == False and game_loop_iteration < game_loop_max_count
    ): 
		game_loop_iteration += 1
		if LOG_STEP_INFO == True:
			print( f"Game loop iteration: {game_loop_iteration}/{game_loop_max_count}\n" )
			cube_client.visualize_cube()

		if game_loop_iteration > game_loop_max_count:
			if LOG_STEP_INFO == True:
				print(f"Breaking game loop, max iterations: {game_loop_max_count}")
			break

		top_row_pieces, bottom_row_pieces, fixable_piece_status = refresh_data()

		game_loop_complete_check = [ is_perfect for _, is_perfect in fixable_piece_status.items() ]
		# print( f"game_loop_complete_check: {game_loop_complete_check}" )
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
		# print( f"fixable_piece_status: {fixable_piece_status}" )
  
		to_side_mappings = {
			cube_client.front_side[1][1]: "front_side",
			cube_client.back_side[1][1]: "back_side",
			cube_client.left_side[1][1]: "left_side",
			cube_client.right_side[1][1]: "right_side"
		}

		all_pieces_to_fix = [ i for i in top_row_pieces if i.get("brick_is_perfect") == False ] +  [ i for i in bottom_row_pieces if i.get("brick_is_perfect") == False ]
		sorted_pieces_to_fix = []

		if len( all_pieces_to_fix ) >= 1:
			extended_moves_not_needed_pieces = []
			needs_extended_moves_pieces = []

			for piece in all_pieces_to_fix:
				needs_extended_move = False
				pieces_parent_data = piece.get("parent_data")
				pieces_parent_side = pieces_parent_data.get("parent_side")
				pieces_parent_row_index = pieces_parent_data.get("parent_row_index")
				pieces_parent_sticker_index = pieces_parent_data.get("parent_sticker_index")

				# print( f"SORTING: {piece}" )

				# TOP ROW EXTENDED MOVE CONDITIONS
				if pieces_parent_side == "top_side" and pieces_parent_row_index == 0:
					needs_extended_move = True
				elif pieces_parent_side == "left_side" and pieces_parent_sticker_index == 0:
					needs_extended_move = True
				elif pieces_parent_side == "right_side" and pieces_parent_sticker_index == 2:
					needs_extended_move = True
				elif pieces_parent_side == "back_side":
					needs_extended_move = True


				# BOTTOM ROW EXTENDED MOVE CONDITIONS
				elif pieces_parent_side == "back_side":
					needs_extended_move = True
				elif pieces_parent_side == "left_side" and pieces_parent_sticker_index == 0:
					needs_extended_move = True
				elif pieces_parent_side == "right_side" and pieces_parent_sticker_index == 2:
					needs_extended_move = True
				elif pieces_parent_side == "bottom_side" and pieces_parent_row_index == 2:
					needs_extended_move = True


				if needs_extended_move == True:
					needs_extended_moves_pieces.append( piece )
				else:
					extended_moves_not_needed_pieces.append( piece )

			sorted_pieces_to_fix = extended_moves_not_needed_pieces + needs_extended_moves_pieces
				
			# print( all_pieces_to_fix )
			# raise Exception(f"LENGTH IS MORE THAN 2, sort this so no extended moves are needed until front side pieces are fixed")
		
		piece_to_fix = sorted_pieces_to_fix[0]

		# if move_extended == True:
		# 	pass

		parent_data = piece_to_fix.get("parent_data")
		parent_side = parent_data.get("parent_side")
		parent_row_index = parent_data.get("parent_row_index")
		parent_sticker_index = parent_data.get("parent_sticker_index")
		fixed_coords = piece_to_fix.get("fixed_coords")
		is_perfect = piece_to_fix.get("brick_is_perfect")
		move_from_to = ( parent_side, parent_row_index, parent_sticker_index, fixed_coords )

		if is_perfect == True:
			print( f"Brick is perfect, moving to next" )
			continue

		# print(f"DATA: {piece_to_fix}")
		# cube_client.visualize_cube()

		if (
			parent_side in ["front_side", "right_side", "back_side", "left_side"]
			and parent_row_index == 0
			or parent_side == "top_side"
		):
			if LOG_STEP_INFO == True:
				print( "Fixing Top Piece" )

			# top color is not on the bottom
			moves_config = {

				# each of these moves below will be needed for destinations: (0, 0), (0, 2), (2, 0), (2, 2)
	
				# TOP FRONT LEFT MOVES
				('top_side', 2, 0, (0, 0)): [
					('rotate_cube', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('rotate_cube', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
					('rotate_cube', 'left', 2),
				],
				('top_side', 2, 0, (0, 2)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 3), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('rotate_cube', 'left', 2), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('rotate_cube', 'left', 2), 
				],
				# ('top_side', 2, 0, (2, 0)): None, # this may not be needed
				('top_side', 2, 0, (2, 2)): [
					('rotate_cube', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('rotate_cube', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
				],
	
				('left_side', 0, 2, (0, 0)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1),
				],
				('left_side', 0, 2, (0, 2)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('move_cube', 'top', 'horizontal', 'left', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'top', 'horizontal', 'right', 1), 
				],
				('left_side', 0, 2, (2, 0)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
					('rotate_cube', 'left', 1),
				],
				('left_side', 0, 2, (2, 2)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1),
				],
	
				('front_side', 0, 0, (0, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1), 
				],
				('front_side', 0, 0, (0, 2)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1),
					('rotate_cube', 'left', 2),
				],
				('front_side', 0, 0, (2, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('rotate_cube', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
				],
				('front_side', 0, 0, (2, 2)): [
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
					
				],
	
				# TOP FRONT RIGHT MOVES
				('top_side', 2, 2, (0, 0)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
				],
				('top_side', 2, 2, (0, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
				('top_side', 2, 2, (2, 0)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
				],
				# ('top_side', 2, 2, (2, 2)): None, # this may not be needed
	
				('right_side', 0, 0, (0, 0)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
				],
				('right_side', 0, 0, (0, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'top', 'horizontal', 'left', 2), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'top', 'horizontal', 'right', 2), 
				],
				('right_side', 0, 0, (2, 0)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
				],
				('right_side', 0, 0, (2, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('rotate_cube', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
	
				('front_side', 0, 2, (0, 0)): [
					('rotate_cube', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 2),
				],
				('front_side', 0, 2, (0, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
				('front_side', 0, 2, (2, 0)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
				],
				('front_side', 0, 2, (2, 2)): [
					('rotate_cube', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
				],
			}

			if move_from_to not in moves_config.keys():
				use_extended_move = False

				if parent_side == "top_side" and parent_row_index == 0:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 2)]
					reverse_extended_moves = [('rotate_cube', 'right', 2)]
				elif parent_side == "left_side" and parent_sticker_index == 0:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 1)]
					reverse_extended_moves = [('rotate_cube', 'left', 1)]
				elif parent_side == "right_side" and parent_sticker_index == 2:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'left', 1)]
					reverse_extended_moves = [('rotate_cube', 'right', 1)]
				elif parent_side == "back_side":
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 2)]
					reverse_extended_moves = [('rotate_cube', 'right', 2)]

				if use_extended_move:
					print("APPLYING EXTENDED MOVE")
					move_extended = True
					for move in extended_moves:
						print( move )
						_, direction, turns = move
						cube_client.rotate_cube( direction, turns )
						steps_to_solve.append( ["rotate_cube", direction, turns] )
					continue

				# TODO: needs pre / post turning for specific moves
				details = f"Fix not implemented for move - {move_from_to}"
				print( details )
				raise Exception( details )
			
			required_moves = moves_config[move_from_to]

			if LOG_STEP_INFO == True:
				print( f"move_from_to used: {move_from_to}" )

			if required_moves == None:
				details = f"required_moves is not configured yet: {move_from_to} - is None"
				print( details )
				raise Exception( details )

			# REVERSE EXTENDED MOVES DATA
			if move_extended == True:
				print("REVERSING EXTENDED MOVE")
				required_moves = required_moves + reverse_extended_moves
				move_extended = False
				extended_moves = []
				reverse_extended_moves = []
			
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

		elif (
			parent_side in ["front_side", "right_side", "back_side", "left_side"]
			and parent_row_index == 2
			or parent_side == "bottom_side"
		):
			if LOG_STEP_INFO == True:
				print( "Fixing Bottom Piece" )

			# top color is not on the bottom

			# lets do this using fewer hard coded moves:
			# 	well need 3 moves for each of the 4 corners on the front
			# 	then if its not defined, turn the cube until one is already defined, 
			# 	then revert turn
			moves_config = {

				# BOTTOM LEFT MOVES (parent coords) 
				# front_side, bottom, left
				# left_side, bottom, right
				# bottom_side, top, left
				# each of these moves ^ will be needed for destinations: (0, 0), (0, 2), (2, 0), (2, 2)
	
				('front_side', 2, 0, (0, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1)
				],
				('front_side', 2, 0, (0, 2)): [
					('rotate_cube', 'left', 2),
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 2),
				],
				('front_side', 2, 0, (2, 0)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
				],
				('front_side', 2, 0, (2, 2)): [
					('rotate_cube', 'left', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
	
				('left_side', 2, 2, (0, 0)): [
					('rotate_cube', 'right', 2),
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 2),
				],
				('left_side', 2, 2, (0, 2)): [
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
				('left_side', 2, 2, (2, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
				],
				('left_side', 2, 2, (2, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
				],
	
				('bottom_side', 0, 0, (0, 0)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'up', 1), 
				],
				('bottom_side', 0, 0, (0, 2)): [
					('move_cube', 'bottom', 'horizontal', 'right', 2), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
				],
				('bottom_side', 0, 0, (2, 0)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 2), 
					('move_cube', 'left', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'left', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'left', 'vertical', 'up', 1), 
				],
				('bottom_side', 0, 0, (2, 2)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
					('move_cube', 'bottom', 'horizontal', 'left', 1), 
					('move_cube', 'right', 'vertical', 'down', 1), 
					('move_cube', 'bottom', 'horizontal', 'right', 1), 
					('move_cube', 'right', 'vertical', 'up', 1), 
				],
	
				# BOTTOM RIGHT MOVES (parent coords)
				# front_side, bottom, right
				# right_side, bottom, left
				# bottom_side, top, right
				# each of these moves ^ will be needed for destinations: (0, 0), (0, 2), (2, 0), (2, 2)
				('front_side', 2, 2, (0, 0)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'left', 'vertical', 'up', 1),  
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'left', 'vertical', 'down', 1),  
						
				],
				('front_side', 2, 2, (0, 2)): [
					('rotate_cube', 'left', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'right', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'up', 1),  
					('rotate_cube', 'right', 1),
				],
				('front_side', 2, 2, (2, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'right', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'up', 1),  
					('rotate_cube', 'left', 1),
				],
				('front_side', 2, 2, (2, 2)): [
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'up', 1),  
				],
					
				('right_side', 2, 0, (0, 0)): [
					('rotate_cube', 'right', 1),
					('move_cube', 'left', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'left', 'vertical', 'up', 1),
					('rotate_cube', 'left', 1),
				],
				('right_side', 2, 0, (0, 2)): [
					('move_cube', 'top', 'horizontal', 'left', 2),
					('move_cube', 'left', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'up', 1),
					('move_cube', 'top', 'horizontal', 'right', 2),
				],
				('right_side', 2, 0, (2, 0)): [
					('move_cube', 'left', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'up', 1),
				],
				('right_side', 2, 0, (2, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'up', 1),  
				],
					
				('bottom_side', 0, 2, (0, 0)): [
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'left', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'right', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1),  
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'up', 1), 
					('rotate_cube', 'left', 1),
				],
				('bottom_side', 0, 2, (0, 2)): [
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('rotate_cube', 'left', 1),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'up', 1),
					('rotate_cube', 'right', 1),
				],
				('bottom_side', 0, 2, (2, 0)): [
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('rotate_cube', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'up', 1),
					('rotate_cube', 'left', 1),
					('move_cube', 'left', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'left', 'vertical', 'up', 1),
				],
				('bottom_side', 0, 2, (2, 2)): [
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 2),
					('move_cube', 'right', 'vertical', 'up', 1),
					('move_cube', 'bottom', 'horizontal', 'right', 1),
					('move_cube', 'right', 'vertical', 'down', 1),
					('move_cube', 'bottom', 'horizontal', 'left', 1),
					('move_cube', 'right', 'vertical', 'up', 1),
				],

			}

			if move_from_to not in moves_config.keys():
				use_extended_move = False

				if parent_side == "back_side":
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 2)]
					reverse_extended_moves = [('rotate_cube', 'right', 2)]
				elif parent_side == "left_side" and parent_sticker_index == 0:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 1)]
					reverse_extended_moves = [('rotate_cube', 'left', 1)]
				elif parent_side == "right_side" and parent_sticker_index == 2:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'left', 1)]
					reverse_extended_moves = [('rotate_cube', 'right', 1)]

				elif parent_side == "bottom_side" and parent_row_index == 2:
					use_extended_move = True
					extended_moves = [('rotate_cube', 'right', 2)]
					reverse_extended_moves = [('rotate_cube', 'right', 2)]

				if use_extended_move:
					print("APPLYING EXTENDED MOVE")
					move_extended = True
					for move in extended_moves:
						print( move )
						_, direction, turns = move
						cube_client.rotate_cube( direction, turns )
						steps_to_solve.append( ["rotate_cube", direction, turns] )
					continue

				# TODO: needs pre / post turning for specific moves
				details = f"Fix not implemented for move - {move_from_to}"
				print( details )
				raise Exception( details )
			
			required_moves = moves_config[move_from_to]

			if LOG_STEP_INFO == True:
				print( f"move_from_to used: {move_from_to}" )

			if required_moves == None:
				details = f"required_moves is not configured yet: {move_from_to} - is None"
				print( details )
				raise Exception( details )

			# REVERSE EXTENDED MOVES DATA
			if move_extended == True:
				print("REVERSING EXTENDED MOVE")
				required_moves = required_moves + reverse_extended_moves
				move_extended = False
				extended_moves = []
				reverse_extended_moves = []
			
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

		else:
			details = f"Piece is not supported: {move_from_to}"
			print( details )
			raise Exception( details )

	if len( step_errors ):
		print( f"Errors in step 2: {step_errors}" )
		raise Exception( f"Errors in step 2: {step_errors}" )
	else:
		# print( [ is_perfect for _, is_perfect in fixable_piece_status.items() ] )
		step_status = "PASS" if False not in [ is_perfect for _, is_perfect in fixable_piece_status.items() ] else "FAIL"

	return step_status, steps_to_solve