import timeit
from statistics import mean, stdev
from modules.cube import RubiksCube

# Number of runs to measure
run_x_times = 1000

def measure_runtime():
    cube_client = RubiksCube()
    cube_client.shuffle_cube(random_turns_count=100)
    cube_client.solve_cube()

# Warm-up phase
for _ in range(10):
    measure_runtime()

# Measure runtimes
runtimes = timeit.repeat('measure_runtime()', 
	setup='from __main__ import measure_runtime', 
	repeat=run_x_times, 
	number=1
)

average_runtime = mean(runtimes)
std_dev_runtime = stdev(runtimes)

print(f"Average runtime over {run_x_times} runs: {average_runtime:.8f} seconds")
print(f"Standard deviation of runtime over {run_x_times} runs: {std_dev_runtime:.8f} seconds")