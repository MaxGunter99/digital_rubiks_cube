
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
### Output:
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