# Graphics
Graphics Team Project
1. MazeSimulator
=> This is the outmost incapsulator for the scripts

2. MazeGenerator
=> This is the maze generator, would be called only once during the total script, will randomly create a maze and print the maze on a 2d array, place traps with in the range that the player could pass without loosing all of its life

3. CharacterController
=> This is the controller that the inputs would be passed to. For the inputs passed here, the the controller would update the users's position, calculate the life loss of the player due to the interaction with traps, and send the results to the graphics generator for showing

4. GraphicsGenerator
=> This is the graphics generator. From this script, the maze would be visulaized to the user.

Requirements

We recommend you to use anaconda to build environment.
Please install numpy, pyopengl, freeglut.

conda install numpy pyopengl, freeglut

How to run the program

cd src

python MazeSimulator.py –h 50 –w 65

(You can designate any other size to build the maze.)


Rules of this Game

1. You cannot pass through the wall.
2. Find a way to the exit point. Compass at the left bottom will indicate the direction to the exit.
3. You can make marks on the floor to indicate important locations or a save point to respawn at a certain point whenever you want.
4. Avoid the traps on the floor. They appear on random spots and are closed and opened regularly. If you fall into the trap, then you will fall and respawn at the beginning of the maze unless you made the save point. If you fall into the trap 5 times, then the save point is reset and you will respawn at the beginning of the maze.

Command
-Move using W, A, S, D
-Rotate using left and right arrow keys.
-Toggle 1st person view / Bird eye view with “B” key.
-Create a mark on the floor with the “M” key.
-Create a save point with the “C” key.
-Load save point with the “L” key.
-Go to the starting point with the “P” key.
