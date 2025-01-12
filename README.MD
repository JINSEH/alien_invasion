# Alien Invasion Game

#### Description
An alien invasion game built with Python and Pygame

Aliens come from top of the screen and will move towards the bottom of the screen.

Players can choose between Easy, Medium and Hard. The difficulty will determine the aliens' initial speed

#### Your objective is to:
1. Shoot down all the aliens before they reach your ship or the bottom of the screen

2. Try and reach a new highscore.

#### How the game ends
The game will continue until the player loses all three lives. After each round, the aliens get faster and faster.

## How to access?
1. Clone my repository
2. Run the alien_invasion.py file.

And you are good to go!

## How did I build the game?
I had to learn pygame's syntax and documentation in order to make use of its functionality. 

1. Next, I created a blank display window and tried to add the ship to it.

2. I added keyboard functionality to it to allow the ship to move.

3. Created bullets sprites and made it come out on top of the ship

4. Created aliens sprites and made it come down the screen.

5. Then record the game statistics and write highscore to json file.