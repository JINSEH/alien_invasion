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

## What each file contains:
Folders include:
1. images
> Contains .bmp files for ship, aliens and stars.

Files include:
1. alien.py
> This file contains the creation of the aliens and its logic, such as: 
>> - what happens when it touches the edge of the screen
>> - Will the alien move right or left
2. alien_invasion.py
> This is the main file which contains the logic for the entirety of the game. 
>> It contains the overall class to manage the game assets and behaviour. 
3. bullets.py
> This file contains the creation of bullets that are fired from the ship. It includes logic such as the movement of the bullets, and redrawing the bullet at each frame of the game.
4. buttons.py 
> This file contains the button builds for the game, mainly before the game starts and when it ends. 
5. gamestats.py
>This file tracks the stats for the game
6. highscore.json
>This file is used to record the highest score. Its logic is written in scoreboard.py
7. scoreboard.py
> This file reports the scoring information and displays it onto the window. 
8. settings.py
> This file contains the settings for the entire game, in this file, you can configure things like the bullets width and initial speed, or the screen resolution.
9. ship.py
> This file is used to manage and create the ship, it contains logic for when the ship should stop moving. 
10. star.py
> This file handles the creation of stars in the background of the game. 