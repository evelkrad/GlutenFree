from settings import *
from sprites import Sprite, MovingSprite, AnimatedSprite, Spike
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell, Pearl
from random import uniform

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()
        self.pearl_sprites = pygame.sprite.Group()


        self.setup(tmx_map, level_frames)

        self.pearl_surf = level_frames['pearl']

    def setup(self, tmx_map, level_frames):
        #Tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x,y,surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semi_collision_sprites)

                match layer:
                    case 'BG': z = Z_LAYERS['bg tiles']
                    case 'FG': z = Z_LAYERS['bg tiles']
                    case _: z = Z_LAYERS['main']
                Sprite((x * TILE_SIZE,y * TILE_SIZE), surf, groups, z)
        
        #Bg details
        for obj in tmx_map.get_layer_by_name('BG details'):
            if obj.name == 'static':
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z = Z_LAYERS['bg tiles'])
            else:
                AnimatedSprite((obj.x, obj.y), level_frames[obj.name], self.all_sprites, z=Z_LAYERS['bg tiles'], animation_speed=ANIMATION_SPEED)
                if obj.name == 'candle':
                    AnimatedSprite((obj.x,obj.y)+ vector(-20,-20),level_frames['candle_light'], self.all_sprites, z = Z_LAYERS['bg tiles'], animation_speed = ANIMATION_SPEED)
              

        #Objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites = self.collision_sprites, 
                    semi_collision_sprites = self.semi_collision_sprites,
                    frames = level_frames['player'])
                
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else: 
                    #frames
                    frames = level_frames[obj.name] if not 'palm' in obj.name else level_frames['palms'][obj.name]
                    if obj.name == 'floor_spike' and obj.properties['inverted']:
                        frames = [pygame.transform.flip(frame, False, True) for frame in frames]
                    #groups
                    groups = [self.all_sprites]
                    if obj.name in('palm_small', 'palm_large'): groups.append(self.semi_collision_sprites)
                    if obj.name in ('saw', 'floor_spike'): groups.append(self.damage_sprites)

                    #z_index
                    z = Z_LAYERS['main'] if not 'bg' in obj.name else Z_LAYERS['bg details']

                    #speed
                    animation_speed = ANIMATION_SPEED if not 'palm' in obj.name else ANIMATION_SPEED + uniform(-1,1)

                    AnimatedSprite((obj.x, obj.y),frames, groups, z, animation_speed)
    
        #Moving Objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):

            if obj.name == 'spike':
                Spike(
                    pos = (obj.x + (obj.width/2), obj.y + (obj.height/2)),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites, self.damage_sprites)
                )
                for i in range(0, obj.properties['radius'],20):
                    Spike(
                    pos = (obj.x + (obj.width/2), obj.y + (obj.height/2)),
                    surf = level_frames['spike_chain'],
                    radius = i,
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites),
                    z = Z_LAYERS['bg details']
                )


            else:
                frames = level_frames[obj.name]
                groups = (self.all_sprites, self.semi_collision_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
                if obj.width > obj.height: #Horizontal
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2 )
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # Vertical
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])


                if obj.name == "saw":
                    if move_dir == 'x':
                        y = start_pos[1]
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x,y),level_frames['saw_chain'] ,self.all_sprites, z = Z_LAYERS['bg details'])
                    else:
                        x = start_pos[0]
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite((x,y),level_frames['saw_chain'] ,self.all_sprites, z = Z_LAYERS['bg details'])

        #Enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)

            if obj.name == 'shell':
                Shell(
                    pos = (obj.x, obj.y),
                    frames = level_frames['shell'], 
                    groups = (self.all_sprites, self.collision_sprites),
                    reverse = obj.properties['reverse'],
                    player = self.player, 
                    create_pearl = self.create_pearl)



    def create_pearl(self, pos, direction):
        Pearl(pos, (self.all_sprites, self.damage_sprites, self.pearl_sprites), self.pearl_surf, direction, 150)

                   

    def pearl_collision(self):
        for sprite in self.collision_sprites:
            pygame.sprite.spritecollide(sprite, self.pearl_sprites, True)

    def hit_collision(self):
        for sprite in self.damage_sprites:
            if sprite.rect.colliderect(self.player.hitbox_rect):
                if hasattr(sprite, 'pearl'):
                    sprite.kill()


    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill('beige')
        self.pearl_collision()
        self.hit_collision()
        self.all_sprites.draw(self.player.hitbox_rect.center)
