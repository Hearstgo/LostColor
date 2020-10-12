import pygame, math, random
from pygame.locals import *

class Monstre1(pygame.sprite.Sprite):
    """ Cette classe represente les objets Monstre1"""
    def __init__(self, spawn_x, spawn_y, target):
        """ Constructeur.
        spawn_x et spawn_ y sont les coordonés d'aparition du monstre
        """
        # Appel du constructeur de la classe mère (Sprite)
        super().__init__()

        #Mise en place de l'image du monstre
        self.image = pygame.image.load('img/blob_0.png')

        self.rect = self.image.get_rect()

        # Mise en place de la cible du monstre
        self.target = target
        
        # Met le monstre au coordonées d'apparition mit en entrée
        self.rect.x = spawn_x
        self.rect.y = spawn_y
        
        # Statistiques du monstre
        self.HP = 100
        self.DMG = 10
        self.speed = random.uniform(2.0, 3.0)

        # rect.x and rect.y sont convertit automatiquement en
        # entiers, on doit créer des variables flotant pour
        # pour contenir les coordonées flotante. Les
        # coordonées entieres ne fournissent pas assez de precision
        # pour la "visé".
        self.floating_point_x = self.rect.centerx
        self.floating_point_y = self.rect.centery


    def calc_angle(self):
        """ Calcul de l'angle"""
        # Créations des coordonées de destination avec le
        # le joueur en entrée
        dest_x = self.target.rect.centerx
        dest_y = self.target.rect.centery

        # Calcul de l'angle en radian entre les coordonées du monstre
        # et le point qu'il vise.
        x_diff = dest_x - self.rect.centerx
        y_diff = dest_y - self.rect.centery
        angle = math.atan2(y_diff, x_diff);

        return angle        


    def update(self):
        """ Déplacement et condition de mort du monstre. """
        # Appel de la méthode pour calculer l'angle
        angle = self.calc_angle()

        # En prenant en compte l'angle on calcul change_x
        # et change_y. La Velocity est la vitesse du monstre.
        
        self.change_x = math.cos(angle) * self.speed
        self.change_y = math.sin(angle) * self.speed
        
        # Les points flotant x et y donne une position plus precise.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # On convertit ces valeur en entier pour rect.x
        # et rect.y pour déplacer le monstre
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

 
        # If the bullet flies of the screen, get rid of it.
        if self.HP <= 0:
            self.kill()