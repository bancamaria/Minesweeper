import abc
import os
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'off'
import pygame
import pygame.locals

class Visualizer(abc.ABC):
    """
    Base class of visualization
    """
    @abc.abstractmethod
    def run(self, runner):
        """
        (Runner) runner - iterator
        """
        pass


class PyGameVisualizer(Visualizer):
    """
    Visualization of the game with PyGame
    """
    SIZE_TILE = 16
    COLOR = (189, 189, 189)
    FILENAME_TILES = os.path.join(os.path.dirname(__file__), 'tiles.png')
    HIDDEN_TILE = 9
    EXPLODED_TILE = 10
    BOMB_TILE = 11
    FLAG_TILE = 12
    WINDOW_NAME = 'Minesweeper'

    def run(self, runner):
        game = runner.game

        self.table_width = game.board_width
        self.table_height = game.board_height

        pygame.init()
        pygame.mixer.quit()  # if we don't turn off sound, uses 100% cpu

        pygame.display.set_caption(self.WINDOW_NAME)
        
        # give the dimensions in pixels of the screen
        screen_pixels_width = self.TILE_SIZE * self.table_width
        screen_pixels_height = self.TILE_SIZE * self.table_height

        # create the screen
        self.screen = pygame.display.set_mode((screen_pixels_width, screen_pixels_height))
        self.screen.fill(self.COLOR)

        # load the tiles
        self.game_tiles = self._load_tiles()

        next(runner) # get the status
        self._draw(game) # update the screen


        if isinstance(self.pause, str):

            print("Move")

            pygame.event.clear()

            while not game.game_over:

                event = pygame.event.wait()

                if event.type == pygame.locals.KEYDOWN:

                    next(runner) # get the status
                    self._draw(game) # update the board

                elif event.type == pygame.locals.QUIT:

                    game.quit()
                    break
        else:

            while not game.game_over:

                time.sleep(self.pause) # wait for a move

                next(runner) # get the status

                self._draw(game) # update the board

        if self.next_game_prompt: # game paused

            print("Hit any key to continue...")

            while True: # render

                event = pygame.event.wait() # wait for an event

                if event.type in [pygame.locals.KEYDOWN, pygame.locals.QUIT]: # resolve that event

                    break

        pygame.quit() # quit the game