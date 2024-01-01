import sys
import pygame

from scripts.entities import PhysicsEntity, Player
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds


class Game:
    def __init__(self):
        pygame.init()

        # Creating window and size
        # Up-scaling so pixel graphics look better
        pygame.display.set_caption('first game')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.movement = [False, False, False, False]

        # Game assets
        self.assets = {
            'decor': load_images('tiles/decor'),
            'grass': load_images('tiles/grass'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'player': load_image('entities/player.png'),
            'background': load_image('background.png'),
            'clouds': load_images('clouds'),
            'player/idle': Animation(load_images('entities/player/idle'), img_duration=6),
            'player/run': Animation(load_images('entities/player/run'), img_duration=4),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide'))
            # 'player': load_image('player/AssetPack-V1/SpriteSheets/player2.png')
        }

        # Create clouds
        self.clouds = Clouds(self.assets['clouds'], count=16)

        # Create player
        self.player = Player(self, (50, 50), (8, 15))

        # Create tilemap
        self.tilemap = Tilemap(self)

        # Camera
        self.scroll = [0, 0]

    def run(self):
        while True:
            # Background color fill
            self.display.blit(self.assets['background'], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)

            # Render tilemap onto display
            self.tilemap.render(self.display, offset=render_scroll)

            # Update and render player with movement based on tilemap and movement
            self.player.update(self.tilemap, [(self.movement[1] - self.movement[0]), 0])
            self.player.render(self.display, offset=render_scroll)

            # X to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Movement controller
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.velocity[1] = -3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False

            # Blit game onto screen
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
