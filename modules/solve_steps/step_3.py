
# STEP 3

# LOG_STEP_INFO = True
LOG_STEP_INFO = False

def solve_cube__step_3( cube_client, test_id=None ):
	"""
    This function should output a list of moves to flip the cube. 
    step format: [ class_function, args ]
    real example: [ 'rotate_cube', 'up', 1 ]

    DESCRIPTION:
        Flip cube upside down so solved is now on the bottom
    """
    
	steps_to_solve = []
	step_status = "FAIL"
	
	if LOG_STEP_INFO == True:
		print( "Starting Step 3!" )

	step_errors = []

	try:
		flip_cube_move = ( "up", 2 )
		direction, turns = flip_cube_move
		cube_client.rotate_cube( direction, turns )
		steps_to_solve.append( flip_cube_move )

		if LOG_STEP_INFO == True:
			cube_client.visualize_cube()
		step_status = "PASS"

		print( "Step 3 - Flip Cube complete" )

	except Exception as e:
		details = f"Error in step 3 flipping cube: {e}"
		step_errors.append( details )

	if len( step_errors ):
		print( f"Errors in step 3: {step_errors}" )
		raise Exception( f"Errors in step 3: {step_errors}" )

	return step_status, steps_to_solve