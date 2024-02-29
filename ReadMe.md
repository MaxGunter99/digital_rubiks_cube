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

- [Initialize & Visualize a Perfect Cube](#example-get-perfect-cube)
- [Initialize, Move & Visualize a Cube](#example-move-cube)

---

<a name="example-get-perfect-cube"></a>

## Initialize & Visualize a Perfect Cube

This will initialize the RubiksCube class, returning a perfect cube. Then Visualize the cube, outputting it to the console.

**Code Example:**
```
cube_client = RubiksCube()
cube_client.visualize_cube()
```

**Visualize Cube Output:**
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

**Code:**
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

**Visualize Cube Output:**

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

## Project Milestones

### Milestone 1: Project Initialization
- **Status:** Completed
- **Description:** This milestone involves initializing the RubiksCube class, setting the cube as a 3D matrix and providing functions which will mutate the cubes data.

### Milestone 2: Implement Vertical Moves ( Up & Down )
- **Status:** Completed
- **Description:** This milestone involves manipulation capabilities by implementing vertical moves.

### Milestone 3: Implement Horizontal Moves ( Left & Right )
- **Status:** In Progress
- **Description:** The next milestone involves extending the cube manipulation capabilities by implementing horizontal moves.

### Milestone 4: Rotating the Cube
- **Status:** Planned
- **Description:** Because we will only be referencing all moves from one side, we'll want to be able to rotate the cube as if you were examining it by hand.

### Milestone 5: Solve Algorithm
- **Status:** Planned
- **Description:** Once horizontal moves and cube rotations are implemented, the project will focus on developing an efficient algorithm to solve the Rubik's Cube. The goal is to create a solution that outputs a list of optimal moves to return the cube to its solved state.

### Milestone 6: Convert to a Python Module
- **Status:** Planned
- **Description:** In this milestone, the project will be transformed into a Python module, allowing users to install and use it as part of their Python projects. This step involves packaging, distribution, and making it available through standard Python package management tools.