"""[summary]
This file is part of the project 'Crazy Funky Dungeon'
You can modify it the way you want but you can't sell it
You can give any ideas that will be read and thought about for the game, 
view readme.md file to know more.
I do not promize that contributions or ideas will be part of this project,
this is a own building project, you are free to use any part of codes, 
and buil your own project on your side and link to me 
I would be glad to see and enjoy your work!
Images aren't free to use, 
all sprites credits to Limzu : https://limezu.itch.io
most of all are from the asset pack Moder Interior
"""

from game import Game
        
if __name__=='__main__':
    game = Game()
    game.show_start_screen()
    
    while True:
        game.new()
        game.run()
        game.show_game_over_screen()