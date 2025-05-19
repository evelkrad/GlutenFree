from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from ui import UI
from overworld import Overworld
from gameover import GameOver
from title import TitleScreen, PauseScreen


class Game:
    def __init__(self):
        pygame.init()
        self.display_serfice = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Gluten Free Quest')
        self.clock = pygame.time.Clock()
        self.import_assets()
        self.game_over_screen = GameOver(self.display_serfice)
        self.game_over_active = False

        title = TitleScreen(self.display_serfice, self.intro_music)
        title.run()
        if title.choice == "controls":
            # Aquí puedes mostrar una pantalla con controles si lo deseas en el futuro
            pass


        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)

        
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', '0.tmx')),
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
            4: load_pygame(join('..', 'data', 'levels', '4.tmx')),   
            5: load_pygame(join('..', 'data', 'levels', '5.tmx'))       
            }
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))
        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
        self.bg_music.play(-1)
        self.bg_music.set_volume(0.2)


    def switch_stage(self, target, unlock = 0):
        if target == 'level':
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files, self.data, self.switch_stage)
            
        else: 
            #Overw
            if unlock > 0:
                self.data.unlocked_level = max(self.data.unlocked_level, unlock)

            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)



    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.game_over_active and event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pause = PauseScreen(self.display_serfice)
                    pause.run()
                    pygame.event.clear()
                    if isinstance(self.current_stage, Level):
                        self.current_stage.paused = True
                        self.current_stage.pause_cooldown = 0.2  # 0.2 segundos de margen


            if self.game_over_active:
                self.audio_files['game_over'].play()
                result = self.game_over_screen.run(events)
                if result == "quit":
                    pygame.quit()
                    exit()
                elif result == "restart":
                    self.data = Data(self.ui)  # Reinicia datos del jugador
                    self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)
                    self.game_over_screen = GameOver(self.display_serfice)  
                    self.game_over_active = False

            else:
                self.current_stage.run(dt)
                self.check_game_over()

            self.ui.update(dt)
            pygame.display.update()




    def import_assets(self):

        water_top = import_folder('..', 'graphics', 'level', 'water','top')
        for frame in water_top:
            frame.set_alpha(150)

        water_body = import_image('..', 'graphics', 'level', 'water','body')
        water_body.set_alpha(150)

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
            'bread': import_folder('..', 'graphics', 'enemies', 'bread', 'run'),
            'shell': import_sub_folders('..','graphics','enemies', 'shell'),
            'pearl': import_image('..','graphics','enemies','bullets','pearl'),
            'items': import_sub_folders('..','graphics','items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'water_top': water_top,
            'water_body': water_body,
            'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'graphics', 'level', 'clouds','small'),
            'cloud_large': import_image('..', 'graphics', 'level', 'clouds','large_cloud'),
        }

        self.font = pygame.font.Font(join('..','graphics','ui','runescape_uf.ttf'), 40)

        self.ui_frames = {
            'heart': import_folder('..','graphics','ui','heart'),
            'coin': import_image('..','graphics','ui','coin'),
        }

        self.overworld_frames = {
            'palms': import_folder('..','graphics','overworld','palm'),
            'water': import_folder('..','graphics','overworld','water'),
            'path': import_folder_dict('..', 'graphics', 'overworld', 'path'),
            'icon': import_sub_folders('..','graphics','overworld', 'icon')
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..','audio','coin.wav')),
            'attack': pygame.mixer.Sound(join('..','audio','attack.wav')),
            'jump': pygame.mixer.Sound(join('..','audio','jump.wav')),
            'damage': pygame.mixer.Sound(join('..','audio','damage.wav')),
            'pearl': pygame.mixer.Sound(join('..','audio','pearl.wav')),
            'death': pygame.mixer.Sound(join('..','audio','death.wav')),
            'game_over': pygame.mixer.Sound(join('..','audio','game_over.wav')),

        }

        self.bg_music = pygame.mixer.Sound(join('..','audio','starlight_city.mp3'))
        self.intro_music = pygame.mixer.Sound(join('..','audio','intro.mp3'))

    def check_game_over(self):
        if self.data.health <= 0:
            self.game_over_active = True


if __name__ == '__main__':
    game = Game()
    game.run()