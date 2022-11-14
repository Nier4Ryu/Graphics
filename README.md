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