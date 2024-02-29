
Project designed by: Michael ( Max ) Gunter

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
# Run Commands:
[Link to Makefile](Makefile)

# Usage Examples:

- [Initialize & Visualize a Perfect Cube](#example-get-perfect-cube)
- [Initialize, Move, and Visualize a Cube](#example-move-cube)

---

<a name="example-get-perfect-cube"></a>

## Initialize & Visualize a Perfect Cube

This will initialize the RubiksCube class, returning a perfect cube. Then Visualize the cube, outputting it to the console.

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

**Visualize Cube Output:**
```

                     Back                     

                ['g', 'g', 'g']                
                ['g', 'g', 'g']                
                ['g', 'g', 'g']                

     Left            Top            Right     

['r', 'r', 'r'] ['w', 'w', 'w'] ['o', 'o', 'o']
['r', 'r', 'r'] ['w', 'w', 'w'] ['o', 'o', 'o']
['r', 'r', 'r'] ['w', 'w', 'w'] ['o', 'o', 'o']

                     Front                     

                ['b', 'b', 'b']                
                ['b', 'b', 'b']                
                ['b', 'b', 'b']                

                    Bottom                    

                ['y', 'y', 'y']                
                ['y', 'y', 'y']                
                ['y', 'y', 'y']                

```

---

<a name="example-move-cube"></a>

## Initialize, Move, and Visualize a Cube

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

     Left            Top            Right     

['r', 'r', 'r'] ['w', 'w', 'g'] ['o', 'o', 'o']
['r', 'r', 'r'] ['w', 'w', 'g'] ['o', 'o', 'o']
['r', 'r', 'r'] ['w', 'w', 'g'] ['o', 'o', 'o']

                     Front                     

                ['b', 'b', 'w']                
                ['b', 'b', 'w']                
                ['b', 'b', 'w']                

                    Bottom                    

                ['y', 'y', 'b']                
                ['y', 'y', 'b']                
                ['y', 'y', 'b']                
```