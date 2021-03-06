import pygame
from constants import *
from pygame.locals import *

class Bonus(pygame.sprite.Sprite):
    """"""
    def __init__(self, bonus_type, gatherer, x=SCREEN_WIDTH//2, y=SCREEN_HEIGHT//2):
        super().__init__()

        self.image = pygame.image.load("img/bonus/"+bonus_type+"_icon.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.bonus_type = bonus_type
        self.gatherer = gatherer
        self.taken = False

    def piked_up(self):
        """"""
        if(pygame.sprite.collide_rect(self, self.gatherer)):
            if (self.bonus_type == "dmg"):
                self.gatherer.DMG_bonus += 2
            elif (self.bonus_type == "heal"):
                self.gatherer.HP += 20
                if self.gatherer.HP > self.gatherer.HP_MAX:
                    self.gatherer.HP = self.gatherer.HP_MAX
            elif (self.bonus_type == "hp_max"):
                self.gatherer.HP_MAX_bonus += 10
                self.gatherer.HP += 10
            elif (self.bonus_type == "shot_speed"):
                self.gatherer.shot_speed_bonus += 1
            elif (self.bonus_type == "speed"):
                self.gatherer.speed_bonus += 0.05
            elif (self.bonus_type == "tps"):
                self.gatherer.tps_bonus += 0.5
            self.gatherer.updateStats()
            self.taken = True
            self.kill()


    def update(self):
        """"""
        self.piked_up()


