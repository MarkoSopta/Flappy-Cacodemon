import pygame as pg
import sys
from caco import *
from pipe import *
from game_objects import *
from settings import *
from fire import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.load_assets()
        self.fire = DoomFire(self)
        self.score=Score(self)
        self.sound = Sound()
        self.new_game()

    def load_assets(self):
        # Cacodemon
        self.caco_images = [pg.image.load(f'assets/caco/{i}.png').convert_alpha() for i in range(5)]
        caco_image = self.caco_images[0]
        caco_size = caco_image.get_width() * CACO_SCALE, caco_image.get_height() * CACO_SCALE
        self.caco_images = [pg.transform.scale(sprite, caco_size) for sprite in self.caco_images]
        # Background       
        self.background_image = pg.image.load('assets/images/bg.png').convert()
        self.background_image = pg.transform.scale(self.background_image, RES)
        # Ground
        self.ground_image = pg.image.load('assets/images/ground.png').convert()
        self.ground_image=pg.transform.scale(self.ground_image,(WIDTH,GROUND_HEIGHT))
        # Pipes
        self.top_pipe_image = pg.image.load('assets/images/pipe.png').convert_alpha()
        self.top_pipe_image = pg.transform.scale(self.top_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.bottom_pipe_image = pg.transform.flip(self.top_pipe_image, False, True)
        # Caco collision mask
        mask_image = pg.image.load('assets/caco/mask.png').convert_alpha()
        mask_size = mask_image.get_width() * CACO_SCALE, mask_image.get_height() * CACO_SCALE
        self.mask_image = pg.transform.scale(mask_image, mask_size)


   
    def new_game(self):

        self.all_sprites_group=pg.sprite.Group()
        self.pipe_group=pg.sprite.Group()
        self.caco=Caco(self)        
        self.background=Background(self)
        self.ground=Ground(self)
        self.pipe_handler = PipeHandler(self)

    def draw(self):

        self.background.draw()
        self.score.draw()
        self.fire.draw()
        self.all_sprites_group.draw(self.screen)
        self.ground.draw()
        self.score.draw()
       # pg.draw.rect(self.screen,"yellow",self.caco.rect,4)
       # self.caco.mask.to_surface(self.screen, unsetcolor=None, dest= self.caco.rect, setcolor='green')
        pg.display.flip()

    def update(self):
        self.background.update()
        self.fire.update()
        self.all_sprites_group.update()
        self.ground.update()
        self.pipe_handler.update()
        self.clock.tick(FPS)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.caco.check_event(event)
        

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()