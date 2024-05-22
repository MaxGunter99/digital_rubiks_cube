
# How do you solve a Rubiks cube?

Describe each step needed to solve a cube, then go into more detail about each step. The solve algorithm will follow.

Focus on one side
1. Solve the top cross
2. Solve the corners
3. Flip cube upside down so solved is now on the bottom
4. Solve on the middle section
5. Solve top cross ( L can match but all top should have yellow on the cross )
6. Corner placement, make sure the corners are in their place, does not have to be solved
7. Solve cube!

---

NEXT, for each section, briefly describe the patterns you are using to solve each part.

1. Solve the top cross
    It needs to be rotated up from one of these sides, left, right, front, back.
    May require turning the top side into the correct spot, will need to rotate back.

2. Solve the corners
    - find corners on outer sides left, right, front, back.
    - match the side color.
    - turn the bottom side horizontally away
    - turn vertical color side towards white piece
    - reverse bottom horizontal turn

    If there are no outer sides left but the top is not solved, check bottom and top
    - align the mismatched pieces horizontally on top of each other, rotate them down and spin the bottom horizontally twice moving the white pieces should be on the outer sides. 
    - Repeat first 5 steps from this section

3. Flip cube upside down so solved is now on the bottom
    rotate cube down 2 times

4. Solve on the middle section
    - find any mismatching piece on the top middle that should be in the middle side
    - align it to the correct side, if it needs to go the the middle right ( else do reverse ):
        - rotate top section horizontally away (left)
        - rotate vertical right up
        - rotate horizontal top left
        - rotate top section horizontally right
        - rotate cube left
        reverse moves from left side
        - rotate the left vertical side up
        - top to the horizontal right
        - left vertical side up
        - top horizontal to the left

        repeat steps until the middle is solved.

        if the piece is reversed and needs to be ejected, repeat the same process as if you are going to insert and try again.

5. Solve top cross ( L can match but all top should have yellow on the cross )
    we need to be able to move the cube pieces without disrupting the solved sections, this should work:
    - rotate the front to the right
    - rotate right up
    - rotate top left
    - rotate right down
    - rotate top right
    -  rotate the front to the left

    repeat steps until the top cross is solved, does not have to match sides, but try to have an L shape of matching sides
    once you have the L, match it to the sides and position it to the back and right, once this is in place follow these moves:
        - right up
        - top left
        - right down
        - top left
        - right up
        - top left 2 times
        - right down
        - top left
    Now the top cross should be solved

6. Corner placement, make sure the corners are in their place, does not have to be solved
    check each corner, if it is in the correct position start with that on the front right and repeat these moves until the top corners are in the correct spots, does not have to be solved, just placement
        - top left
        - right up
        - top right
        - left up
        - top left
        - right down
        - top right
        - left down
    if non corners were matching, they should have moved, check to see any matching and move it to the right.
    - repeat steps until corners are placed correctly
    
7. Flip cube upside down so solved is now on the bottom
    rotate cube down 2 times

8. Solving the cube!!
    if any corners are in the correct spot, start by rotating the cube to the right, if the next piece is solved keep rotating it to the right so you start with an unsolved corner.
    once the unsolved corner is in place, repeat these steps until the corner is solved!:
        - right up
        - top left
        - right down
        - top left
    once corner is its solved:
        - rotate bottom to right
        - repeat steps above
    once all the corners are solved, it should only require rotating the bottom to get a perfect cube!!

    