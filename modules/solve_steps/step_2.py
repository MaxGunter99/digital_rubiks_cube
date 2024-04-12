
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


		# ... step logic
		raise Exception( "STEP NOT IMPLEMENTED" )

	if len( step_errors ):
		print( f"Errors in step 2: {step_errors}" )
		raise Exception( f"Errors in step 2: {step_errors}" )

	return step_status, steps_to_solve