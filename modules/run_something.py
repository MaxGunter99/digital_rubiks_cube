

def run_something(side):

    thing_1 = "thing 1"
    thing_2 = "thing 2"

    side_index_map = {
        "left": 0,
        "middle": 1,
        "right": 2
    }

    for i in range( 3 ):
        for x in range( 3 ):

            # I want the second index == 1 to replicate moving the middle side up
            if x == side_index_map[side]:
                thing = thing_2
            else:
                thing = thing_1 # ( static sides )
            print_data = {
                "thing": thing,
                "i": i,
                "x": x
            }
            print( print_data )

run_something()