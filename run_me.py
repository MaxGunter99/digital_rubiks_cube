
import os
from pprint import pprint
from modules.cube import RubiksCube

# WIP:

# We need some kind of game loop...
# For now we can call a class to be able to keep the class rubiks cube shape

# def game_loop(
#     cube = None
# ): 
#     # compare to perfect cube
#     # compare side sequences, this is max efficient
#     if cube:
#         return "No Cube"
#     # while cube

os.system("clear")


# Successful Functions Here ( w/ call functions ):
# Makeshift version control

def get_game_client():
    cube_client = RubiksCube()
    return cube_client

def get_perfect_cube():
    """
    Returns perfect_cube
    """

    cube_client = RubiksCube()
    cube = cube_client.cube
    # pprint( cube )

    return cube


# "Run this file" for testing purposes 
# utilize this in make commands:

# perfect_cube = get_perfect_cube()
# visualize_cube( perfect_cube )




# USE FOR FUTURE TESTS -- DO NOT DELETE --:

# Class Introduction:
# cube_client = RubiksCube()

# ---

# visualize_cube( cube_client ) # PERFECT CUBE
# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# visualize_cube( cube_client ) # The top section should have turned clockwise!
# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )
# visualize_cube( cube_client ) # Should reverse it back to a PERFECT CUBE

# ---

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# visualize_cube( cube_client ) # middle shift clockwise

# ---

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )
# visualize_cube( cube_client ) # middle shift counterclockwise

# ---

# MINI SHUFFLE

# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )
# visualize_cube( cube_client )

# SINGLE MOVE TESTING:

# cube_client.move_cube(
#     section="middle",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )
# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )
# this move below needs work, it will always move the middle up too
# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )
# CONTINUE HERE
# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.visualize_cube()

# ---

# WIP: look into elif direction == "counterclockwise":
# USE FOR FUTURE TESTS -- DO NOT DELETE --:






cube_client = RubiksCube()

# ------- COMPLETED MOVES -------

# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )

# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="up",
#     turns=1
# )

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )

# pprint( cube_client.raw_cube )

# cube_client.rotate_cube("left", 1)
# cube_client.rotate_cube("right", 1)
# cube_client.rotate_cube("up", 1)
# cube_client.rotate_cube("down", 1)

# ------ manual testing with physical cube -------

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.rotate_cube("left", 1)
# cube_client.rotate_cube("down", 5)

# PASSES

# ---

# cube_client.move_cube(
#     section="middle",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )

# cube_client.rotate_cube("left", 1)
# cube_client.rotate_cube("down", 5)

# -----

# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.rotate_cube("left", 2)
# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# PASSES - perfect cube just turned around

# -------

# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.rotate_cube("right", 2)
# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )

# PASSES - perfect cube just turned around

# -------

# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# cube_client.rotate_cube("down", 2)
# cube_client.move_cube(
#     section="bottom",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )

# PASSES - perfect cube

# -------

# cube_client.move_cube(
#     section="bottom",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )
# cube_client.rotate_cube("up", 2)
# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="right",
#     turns=1
# )
# PASSES - perfect cube

# -------

# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# cube_client.rotate_cube("up", 2)
# cube_client.move_cube(
#     section="left",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.rotate_cube("down", 1)
# cube_client.rotate_cube( "left", 2 )
# cube_client.move_cube(
#     section="right",
#     orientation="vertical",
#     direction="down",
#     turns=1
# )
# cube_client.rotate_cube( "down", 1 )
# cube_client.move_cube(
#     section="middle",
#     orientation="horizontal",
#     direction="left",
#     turns=5
# )
# PASSES - perfect cube

# cube_client.shuffle_cube( random_turns_count=10 )
# print("------")
# cube_client.print_tracked_moves()

# STEP 1 MANUAL TESTING
# cube_client.move_cube(
#     section="bottom",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )
# cube_client.move_cube(
#     section="top",
#     orientation="horizontal",
#     direction="left",
#     turns=1
# )

# STEP 2 TESTING
# cube_client.shuffle_cube( random_turns_count=100 )
# # print(  f"Steps to recreate cube: {cube_client.tracked_moves}" )
# cube_client.visualize_cube()
# steps_to_solve = cube_client.solve_cube( step_override=2 )
# cube_client.visualize_cube()
# # print(  f"Steps to solve cube: {steps_to_solve}" )
# # cube_client.check_sides()

# STEP 3 TESTING
# cube_client.shuffle_cube( random_turns_count=100 )
# # print(  f"Steps to recreate cube: {cube_client.tracked_moves}" )
# cube_client.visualize_cube()
# steps_to_solve = cube_client.solve_cube( step_override=3 )
# cube_client.visualize_cube()
# # print(  f"Steps to solve cube: {steps_to_solve}" )
# # cube_client.check_sides()

# STEP 4 TESTING
cube_client.shuffle_cube( random_turns_count=100 )
# print(  f"Steps to recreate cube: {cube_client.tracked_moves}" )
cube_client.visualize_cube()
steps_to_solve = cube_client.solve_cube( step_override=4 )
cube_client.visualize_cube()
# print(  f"Steps to solve cube: {steps_to_solve}" )
# cube_client.check_sides()



# FOR SORTING DICTIONARY KEYS
# from_to_move_config = {
# 
# }

# # print( sorted( from_to_move_config ) )
# for key in sorted( from_to_move_config ):
#     print( f"{key}: {from_to_move_config[key]}," )
