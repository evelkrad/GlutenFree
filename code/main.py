from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_serfice = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gluten Free Quest')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.tmx_maps = {0: load_pygame(join('..', 'data', 'levels', 'omni.tmx'))}
        self.current_stage = Level(self.tmx_maps[0], self.level_frames)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.current_stage.run(dt)
            pygame.display.update()

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..','graphics','level','flag'),
            'saw' : import_folder('..','graphics','enemies','saw','animation'),
            'saw_chain': import_image('..','graphics','enemies','saw','saw_chain'),
            'floor_spike' : import_folder('..','graphics','enemies','floor_spikes'),
            'palms': import_sub_folders('..','graphics','level','palms'),
            'candle': import_folder('..','graphics','level','candle'),
            'window': import_folder('..','graphics','level','window'),
            'big_chain': import_folder('..','graphics','level','big_chains'),
            'small_chain': import_folder('..','graphics','level','small_chains'),
            'candle_light': import_folder('..','graphics','level','candle light'),
            'player': import_sub_folders('..','graphics','player'),
            'helicopter' : import_folder('..','graphics','level','helicopter'),
            'boat' : import_folder('..','graphics','objects','boat'),
            'spike': import_image('..','graphics','enemies','spike_ball','Spiked Ball'),
            'spike_chain': import_image('..','graphics','enemies','spike_ball','spiked_chain'),
            'tooth': import_folder('..', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..','graphics','enemies', 'shell'),
            'pearl': import_image('..','graphics','enemies','bullets','pearl'),
        }

if __name__ == '__main__':
    game = Game()
    game.run()