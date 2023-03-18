import pygame as pg
from settings import *
from collections import deque   
class Caco(pg.sprite.Sprite):
    
    def __init__(self, game):
        super().__init__(game.all_sprites_group)
        self.game= game
        self.image= game.caco_images[0]
        self.mask=pg.mask.from_surface(game.mask_image)
        self.rect= self.image.get_rect()
        self.rect.center=CACO_POS

        self.images= deque(game.caco_images)
        self.animation_event=pg.USEREVENT+0
        pg.time.set_timer(self.animation_event,CACO_ANIMATION_TIME)

        self.falling_velocity=0
        self.initial_jump = False
        self.angle=0

    def rotate(self):
        if self.initial_jump:
            if self.falling_velocity<-JUMP_VALUE:
                self.angle=JUMP_ANGLE
            else:
                self.angle=max(-2.5*self.falling_velocity,-90)    
            self.image=pg.transform.rotate(self.image,self.angle)    
            # new mask
            mask_image = pg.transform.rotate(self.game.mask_image,self.angle)
            self.mask = pg.mask.from_surface(mask_image)


    def collision_check(self):
        

        hit = pg.sprite.spritecollide(self, self.game.pipe_group, dokill=False,
                                      collided=pg.sprite.collide_mask)
        if hit or self.rect.bottom >GROUND_Y or self.rect.top < -self.image.get_height():
            self.game.sound.hit_sound.play()
            pg.time.wait(1500)
            self.game.new_game()


    def jump(self):

        self.game.sound.jump_sound.play()
        self.initial_jump=True
        self.falling_velocity=JUMP_VALUE    

    def force_of_gravity(self):
        if self.initial_jump:
            self.falling_velocity+=GRAVITY
            self.rect.y +=self.falling_velocity + 0.5 * GRAVITY

    def update(self):
        self.collision_check()
        self.force_of_gravity()    
   
    def animate(self):
        self.images.rotate(-1)
        self.image=self.images[0]
   
    def check_event(self,event):
        if event.type==self.animation_event:
            self.animate()
            self.rotate()
        if event.type== pg.MOUSEBUTTONDOWN:
            if event.button==1:
                self.jump()
            