```
   _ _ _
  /_/_/_/\
 /_/_/_/\/\
/_/_/_/\/\/\
\_\_\_\/\/\/
 \_\_\_\/\/
  \_\_\_\/

 ______   __  __   ______   __   __  __   ______       ______   __  __   ______   ______    
/\  == \ /\ \/\ \ /\  == \ /\ \ /\ \/ /  /\  ___\     /\  ___\ /\ \/\ \ /\  == \ /\  ___\   
\ \  __< \ \ \_\ \\ \  __< \ \ \\ \  _"-.\ \___  \    \ \ \____\ \ \_\ \\ \  __< \ \  __\   
 \ \_\ \_\\ \_____\\ \_____\\ \_\\ \_\ \_\\/\_____\    \ \_____\\ \_____\\ \_____\\ \_____\ 
  \/_/ /_/ \/_____/ \/_____/ \/_/ \/_/\/_/ \/_____/     \/_____/ \/_____/ \/_____/ \/_____/ 
                  
```

Project designed by: Michael ( Max ) Gunter

## Overview:

This is an interactive Python project that brings the classic Rubik's Cube into the digital realm. This project leverages a sophisticated Python 3D matrix data structure to store and manipulate the values of each side of the Rubik's Cube

## Run Commands:
[Link to Makefile](Makefile)

## Getting Started:

- [Initialize Perfect Cube](#example-get-perfect-cube)
- [Move & Visualize a Cube](#example-move-cube)
- [Cube Rotation](#example-rotate-cube)
- [Shuffle Cube Randomly](#example-shuffle-cube-randomly)
- [Printing Moves Applied](#example-print-moves-applied)
- [Running the Solve Cube Algorithm](#example-solve-cube)

---

<a name="example-get-perfect-cube"></a>

## Initialize & Visualize a Perfect Cube

This will initialize the RubiksCube class, returning a perfect cube. Then Visualize the cube, outputting it to the console.

**Code Example:**
```
cube_client = RubiksCube()
cube_client.visualize_cube()
```

**Output:**
```
                     Back                     

                ['g', 'g', 'g']                
                ['g', 'g', 'g']                
                ['g', 'g', 'g']                

                      Top                      

                ['w', 'w', 'w']                
                ['w', 'w', 'w']                
                ['w', 'w', 'w']                

     Left           Front           Right     

['r', 'r', 'r'] ['b', 'b', 'b'] ['o', 'o', 'o']
['r', 'r', 'r'] ['b', 'b', 'b'] ['o', 'o', 'o']
['r', 'r', 'r'] ['b', 'b', 'b'] ['o', 'o', 'o']

                    Bottom                    

                ['y', 'y', 'y']                
                ['y', 'y', 'y']                
                ['y', 'y', 'y']
```

---

<a name="example-move-cube"></a>

## Initialize, Move & Visualize a Cube

This will initialize the RubiksCube class, then the cube will be mutated, moving the right vertical section down. After the cube has mutated we will be able to visualize it.

**Code Example:**
```
cube_client = RubiksCube()

cube_client.move_cube(
   section="right",
   orientation="vertical",
   direction="down",
   turns=1
)

cube_client.visualize_cube()
```

**Output:**

```
                     Back                     

                ['y', 'g', 'g']                
                ['y', 'g', 'g']                
                ['y', 'g', 'g']                

                      Top                      

                ['w', 'w', 'g']                
                ['w', 'w', 'g']                
                ['w', 'w', 'g']                

     Left           Front           Right     

['r', 'r', 'r'] ['b', 'b', 'w'] ['o', 'o', 'o']
['r', 'r', 'r'] ['b', 'b', 'w'] ['o', 'o', 'o']
['r', 'r', 'r'] ['b', 'b', 'w'] ['o', 'o', 'o']

                    Bottom                    

                ['y', 'y', 'b']                
                ['y', 'y', 'b']                
                ['y', 'y', 'b']
```

---

<a name="example-rotate-cube"></a>

## Cube Rotation

Cube rotation allows us to operate all given moves on any side of the cube just by rotating it to the desired side.

**Code Example:**
```
cube_client = RubiksCube()

cube_client.rotate_cube(
   direction="left", 
   turns=1
)
cube_client.visualize_cube()
``````

**Output:**

```
                     Back                     

                ['r', 'r', 'r']                
                ['r', 'r', 'r']                
                ['r', 'r', 'r']                

                      Top                      

                ['w', 'w', 'w']                
                ['w', 'w', 'w']                
                ['w', 'w', 'w']                

     Left           Front           Right     

['b', 'b', 'b'] ['o', 'o', 'o'] ['g', 'g', 'g']
['b', 'b', 'b'] ['o', 'o', 'o'] ['g', 'g', 'g']
['b', 'b', 'b'] ['o', 'o', 'o'] ['g', 'g', 'g']

                    Bottom                    

                ['y', 'y', 'y']                
                ['y', 'y', 'y']                
                ['y', 'y', 'y'] 
```

---

<a name="example-shuffle-cube-randomly"></a>

## Shuffling a Cube Randomly

Getting a random cube can be used with the `cube_client.shuffle_cube()` function. This takes two arguments, the integer `random_turns_count`. To exclude random rotations, this can be disabled by passing `disable_rotations=True` when calling `shuffle_cube`, resulting in only applying moves to the front side of the cube

**Code Example:**
```
cube_client = RubiksCube()
cube_client.shuffle_cube( random_turns_count=5 )
``````

**Output:**

```
                     Back                     

                ['g', 'w', 'g']                
                ['g', 'w', 'g']                
                ['o', 'w', 'r']                

                      Top                      

                ['w', 'b', 'w']                
                ['w', 'g', 'y']                
                ['w', 'o', 'y']                

     Left           Front           Right     

['r', 'r', 'r'] ['o', 'w', 'r'] ['g', 'g', 'b']
['o', 'o', 'o'] ['b', 'y', 'b'] ['r', 'r', 'r']
['b', 'b', 'g'] ['b', 'y', 'b'] ['o', 'o', 'o']

                    Bottom                    

                ['w', 'r', 'y']                
                ['y', 'b', 'y']                
                ['y', 'g', 'y']                
```

---

<a name="example-print-moves-applied"></a>

## Printing Moves Applied

To physically recreate a cube you have mutated here, simply log all of the tracked moves by using the `cube_client.print_tracked_moves()` function. This will output all rotations and moves to the console. Follow step by step to have a physical copy.

An important note, cube rotations do not count as "moves" because the cube remains unchanged when rotating, in this example we will shuffle the cube 5 times but the cube will be randomly rotated applying moves to any side. To exclude random rotations, this can be disabled by passing `disable_rotations=True` when calling `shuffle_cube`

**Code Example:**
```
cube_client = RubiksCube()
cube_client.shuffle_cube( random_turns_count=5 )
cube_client.print_tracked_moves()
cube_client.visualize_cube()
```

**Output:**

```
{'action': 'move_cube', 'section': 'middle', 'orientation': 'vertical', 'direction': 'up', 'turns': 2}
{'action': 'rotate_cube', 'direction': 'left', 'turns': 1}
{'action': 'move_cube', 'section': 'middle', 'orientation': 'horizontal', 'direction': 'left', 'turns': 1}
{'action': 'rotate_cube', 'direction': 'up', 'turns': 1}
{'action': 'move_cube', 'section': 'top', 'orientation': 'horizontal', 'direction': 'right', 'turns': 1}
{'action': 'rotate_cube', 'direction': 'up', 'turns': 1}
{'action': 'move_cube', 'section': 'middle', 'orientation': 'horizontal', 'direction': 'right', 'turns': 1}
{'action': 'move_cube', 'section': 'middle', 'orientation': 'horizontal', 'direction': 'right', 'turns': 1}

                     Back                     

                ['o', 'g', 'o']                
                ['b', 'g', 'b']                
                ['o', 'g', 'o']                

                      Top                      

                ['b', 'o', 'b']                
                ['w', 'w', 'w']                
                ['y', 'y', 'y']                

     Left           Front           Right     

['w', 'g', 'b'] ['r', 'r', 'r'] ['g', 'b', 'y']
['r', 'r', 'y'] ['o', 'b', 'o'] ['w', 'o', 'o']
['w', 'g', 'b'] ['r', 'r', 'r'] ['g', 'b', 'y']

                    Bottom                    

                ['w', 'w', 'w']                
                ['y', 'y', 'y']                
                ['g', 'r', 'g']   
```

---

<a name="example-solve-cube"></a>

## Running the Solve Cube Algorithm

This example showcases how to run the solve algorithm which utilizes the `solve_cube` function. This will return a list of steps needed to solve a given (or randomly shuffled) cube

We'll use a random shuffle of 100 moves, print those moves if you would like to recreate it with your own cube. To asolve the first step - the top cross pass an `int` as `step_override` will stop the algorithm at the specified step number. Passing 7 or leaving this blank should return a fully solved cube. At the end we'll print the solve steps

**Code Example:**
```
cube_client.shuffle_cube( random_turns_count = 100 )
print(  f"Steps to recreate cube: {cube_client.tracked_moves}" )
cube_client.visualize_cube()
steps_to_solve = cube_client.solve_cube( step_override = 1 )
cube_client.visualize_cube()
print(  f"Steps to solve cube: {steps_to_solve}" )
```

---

## Project Milestones

### Milestone 1: Project Initialization
- **Status:** Completed
- **Description:** This milestone involves initializing the RubiksCube class, setting the cube as a 3D matrix and providing functions which will mutate the cubes data.

### Milestone 2: Writing Tests
- **Status:**  In Progress
- **Description:** This project has been powered by test driven development, curiosity, and the iterative process. This milestone is to ensure all moves are covered properly by writing tests. A manual but invaluable asset. Testing every move will ensure the algorithms reliability, we do not scramble our cube making it impossible to solve. We will also require TDD for the solve algorithm

### Milestone 3: Implement Vertical Moves ( Up & Down )
- **Status:** Completed
- **Description:** This milestone involves manipulation capabilities by implementing vertical moves.

### Milestone 4: Implement Horizontal Moves ( Left & Right )
- **Status:** Completed
- **Description:** This milestone involves completing the cube manipulation capabilities by implementing horizontal moves.

### Milestone 5: Rotating the Cube
- **Status:** Completed
- **Description:** Because we will only be referencing all moves from one side, we'll want to be able to rotate the cube as if you were examining it by hand.

### Milestone 6: Solve Algorithm
- **Status:** In Progress
- **Description:** Once testing is completed, the project will focus on developing an efficient algorithm to solve a Rubik's Cube. The goal is to create a solution that outputs a list of optimal moves to return the cube to its solved state.

*Milestone 6 Breakdown:*

**Solve Reference Documentation**: [Link to Solve Steps](SolveCubeSteps.md)
- Step 1: Top Cross - ✅
- Step 2: Corners Around Top Cross - ✅
- Step 3: Flip Cube - IN PROGRESS
- Step 4: Middle Section - ❌
- Step 5: Opposite Sides Top Cross - ❌
- Step 6: Opposite Sides Corner Placement - ❌
- Step 7: Ordering Opposite Sides Corners - ❌


### Milestone 7: Refactoring
- **Status:** Planned
- **Description:** This milestone entails refactoring the solve steps, focusing on significant enhancements. All changes will be meticulously tested to guarantee continued solvability of cubes before refactoring.

### Milestone 8: Convert to a Python Module
- **Status:** Planned
- **Description:** In this milestone, the project will be transformed into a Python module, allowing users to install and use it as part of their Python projects. This step involves packaging, distribution, and making it available through standard Python package management tools.