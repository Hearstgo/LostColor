from menu import *
from constants import *
from Bullet import *
from Ennemis import *
from Bonus import *
from player import *
from Room import *
import random
from math import sqrt

def initPartie():
    """"""
    etage = []

def initSprites():
    global all_sprites_list,enemy_list,bullet_list,player,rooms,current_room_no,current_room
    # --- Listes de Sprites
    # Ceci est la liste de tous les sprites. Tous les ennemis et le joueur aussi.
    # Un groupe de sprite LayeredUpdates possede en plus un ordre (pour l'affichage)
    all_sprites_list = pygame.sprite.LayeredUpdates()


    # Liste des balles
    bullet_list = pygame.sprite.Group()

    # --- Creation des Sprites
    # Création du joueur
    player = Player("Test", 0, 0, 6)

    player.rect.centerx = 2 * SCREEN_WIDTH // 3
    player.rect.centery = 2 * SCREEN_HEIGHT // 3

    # Création des salles
    rooms = []
    # Ajout de la première salle ("Tuto")
    room = RoomTuto(player)
    rooms.append(room)

    # Ajout des salles normales
    # room = RoomNormal()
    # rooms.append(room)
    # A voir

    # Salle courante (ou est le joueur est)
    current_room_no = 0
    current_room = rooms[current_room_no]


    # Ajout des sprite dans l'ordre d'affichage dans le Group all_sprites_list
    all_sprites_list.add(current_room.enemy_list)
    all_sprites_list.add(bullet_list)
    all_sprites_list.add(player)


def spawnNMonsters(N,color="none"):
    """Cette fonction fait appraitre N enemies"""
    for i in range(0, N):
        monstre = Monstre1(random.randint(0, SCREEN_WIDTH),
                           random.randint(0, SCREEN_HEIGHT // 3),
                           player)
        if color!="none":
            monstre.setColor(color)
        current_room.enemy_list.add(monstre)
        all_sprites_list.add(monstre)



def draw_text(screen,text, font_name, size, color, x, y, center):
    """"""
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.centerx = x
        text_rect.centery = y
    else:
        text_rect.x = x
        text_rect.y = y

    screen.blit(text_surface, text_rect)

def draw_HUD(screen):
    """Head up display : affichage d'information pour le joueur"""

    # Affichage PV
    draw_text(screen, "PV : " + str(player.HP) + "/" + str(player.HP_MAX), 'fonts/RPGSystem.ttf', 20, BLACK, 25, SCREEN_HEIGHT//2+20, False)

    # Affichage DMG
    draw_text(screen, "DMG : " + str(player.DMG), 'fonts/RPGSystem.ttf', 20, BLACK, 25, SCREEN_HEIGHT // 2, False)

    # Affichage TPS
    draw_text(screen, "TPS : " + str(player.tps), 'fonts/RPGSystem.ttf', 20, BLACK, 25, SCREEN_HEIGHT // 2 - 20, False)

    # Affichage SPEED
    draw_text(screen, "SPEED : " + str(player.speed), 'fonts/RPGSystem.ttf', 20, BLACK, 25, SCREEN_HEIGHT // 2 - 40, False)

    # Affichage SPEED
    draw_text(screen, "SHOT SPEED : " + str(player.shot_speed), 'fonts/RPGSystem.ttf', 20, BLACK, 25, SCREEN_HEIGHT // 2 - 60, False)


def setNewPolygones():
    res=[]
    for p in polygones_list:
        randomX= randint(0,SCREEN_WIDTH)
        randomY = randint(0,SCREEN_HEIGHT)
        newp=[]
        for point in p:
            newp+=[((randomX+point[0])/2,(randomY+point[1])/2)]
        res+=[[newp,random.choice(COLORS)]]

    return res

def drawPolygones(screen,poly_list):
    for p in poly_list:
        pygame.draw.polygon(screen, p[1], p[0],0)


def main_menu(screen,fpsClock):
    running = True
    click = False
    #créer les boutons
    b1 = Bouton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, 'Jouer', RED)
    b2 = Bouton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 'Options', GREEN)
    b3 = Bouton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, 'Credit', BLUE)
    b4 = Bouton(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, 'Quitter', GRAY)

    while running:
        #fermeture de la fenetre
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #clic de la souris
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        #on recupère les coordonnées de la souris
        mx, my = pygame.mouse.get_pos()

        #Si l'utilisateur clique sur un bouton, on lance la fonction adaptée
        if b1.hoover(mx, my):
            if click:
                game(screen,fpsClock)
        if b2.hoover(mx, my):
            if click:
                pass # options()
        if b3.hoover(mx, my):
            if click:
                pass # credits()
        if b4.hoover(mx, my):
            if click:
                pygame.quit()
                sys.exit()

        #affichage 
        screen.fill((255, 255, 255))
        #affiche le nom du jeu
        draw_text(screen,'Lost color', 'fonts/No_Color.ttf', 60, BLACK, SCREEN_WIDTH // 2, 100, True)
        #affiche les boutons
        b1.draw(screen, mx, my)
        b2.draw(screen, mx, my)
        b3.draw(screen, mx, my)
        b4.draw(screen, mx, my)
        #on passe click a false pour pas que le jeu considère que l'utilisateur clique sans arrêt.
        click = False

        pygame.display.update()
        fpsClock.tick(FPS)



def game(screen,fpsClock):
    playing = True
    n=random.randint(3,10)
    taches=createNTaches(n,(6,20))
    cd=0
    while playing:

        # --- Gestion des Event
        for event in pygame.event.get():

            # close game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Detection d'utilisation du clavier pour faire spawner 3 monstres
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP8:
                    spawnNMonsters(3)
                if event.key == pygame.K_KP1:
                    bonus_test = Bonus("dmg", player)
                    all_sprites_list.add(bonus_test)
                if event.key == pygame.K_KP2:
                    bonus_test = Bonus("tps", player)
                    all_sprites_list.add(bonus_test)
                if event.key == pygame.K_KP3:
                    bonus_test = Bonus("shot_speed", player)
                    all_sprites_list.add(bonus_test)
                if event.key == pygame.K_KP4:
                    bonus_test = Bonus("heal", player)
                    all_sprites_list.add(bonus_test)
                if event.key == pygame.K_KP5:
                    bonus_test = Bonus("hp_max", player)
                    all_sprites_list.add(bonus_test)
                if event.key == pygame.K_KP6:
                    bonus_test = Bonus("speed", player)
                    all_sprites_list.add(bonus_test)
                if event.key == K_ESCAPE:
                    playing = False
                if event.key == K_1:
                    player.colorbuff=GRAY
                if event.key == K_2:
                    player.colorbuff=RED

        # Detection d'utilisation du clavier pour déplacer le joueur:

        activeKey = pygame.key.get_pressed()

        if activeKey[K_a]:  # left
            player.move("LEFT", current_room.wall_list)
        if activeKey[K_d]:  # right
            player.move("RIGHT", current_room.wall_list)
        if activeKey[K_w]:  # top
            player.move("UP", current_room.wall_list)
        if activeKey[K_s]:  # bottom
            player.move("DOWN", current_room.wall_list)

        #on change la couleur du joueur en fonction de la position 
        setColorPlayerFromPosition(taches,player)

        #on met a jour les stats des monstres en fonction de la couleur du joueur
        if cd ==120:
            manageWhiteMobs(current_room.enemy_list)
            cd=0
        updateMobsStats(current_room.enemy_list,player.colorbuff)
        # shoot
        activeMouse = pygame.mouse.get_pressed()
        # print(activeMouse)
        if activeMouse[0] == True:
            if player.cooldown >= player.cooldown_max:
                # position de la souris
                pos = pygame.mouse.get_pos()

                mouse_x = pos[0]
                mouse_y = pos[1]

                # Créé la balle
                bullet = Bullet(player, mouse_x, mouse_y, player.colorbuff)

                # et l'ajoute a la liste des balles
                bullet_list.add(bullet)
                all_sprites_list.add(bullet)
                # Remise à 0 du temps de rechargement de tire
                player.cooldown = 0

        # --- Logique du jeu
        for bullet in bullet_list:

            # Si une balle touche un monstre
            enemy_hit_list = pygame.sprite.spritecollide(bullet, current_room.enemy_list, False)

            # Pour chaque monstre touché, on supprime la balle et on fait perdre de la vie au monstre en fonction de la couleur de la balle
            for mob in enemy_hit_list:
                dmgDone=False
                
                # Lorsqu'un ennemie se fait toucher il perd les dégats du joueur si il n'est pas de la m
                if bullet.color==GRAY:
                    mob.HP -= player.DMG*0.5
                    dmgDone=True
                elif bullet.color!=mob.colorbuff:
                    mob.HP -= player.DMG*1.5
                    dmgDone=True

                if dmgDone:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

            # On supprime la balle de la liste des sprites si elle sort de l'écran
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        # Colision entre joueur et monstre
        for mob in current_room.enemy_list:
            if pygame.sprite.collide_rect(mob, player) and not player.get_hit:
                player.get_hit = True
                player.HP -= mob.DMG



        # Appelle la méthode update() de tous les Sprites
        all_sprites_list.update()

        # Méthode update de la salle courante pour la gestion des portes
        current_room.update()

        # --- Dessiner la frame
        # Clear the screen
        screen.fill(WHITE)
        #affiche a nouveau les taches
        drawAllTaches(screen,taches)
        # Dessine tous les sprites (les blits sur screen)
        all_sprites_list.draw(screen)
        # Dessine les murs et portes de la salle courante
        current_room.wall_list.draw(screen)
        current_room.door_list.draw(screen)

        # Affichage HUD
        draw_HUD(screen)


        cd+=1
        # Met à jour la fenetre de jeu
        pygame.display.update()

        # --- Limite le jeu à 60 images par seconde
        fpsClock.tick(FPS)
        

def updateMobsStats(mobs_lists,color):
    for mob in mobs_lists:
        if mob.colorbuff == color and not mob.isboosted:
            mob.DMG*=2
            mob.speed+=3
            mob.isboosted=True
        elif mob.colorbuff != color and mob.isboosted:
            mob.DMG/=2
            mob.speed-=3
            mob.isboosted=False

def manageWhiteMobs(mobs_lists):
    is_colored_mob=False

    for mob in mobs_lists:
        if mob.colorbuff != GRAY:
            is_colored_mob=True

    if is_colored_mob:
        spawnNMonsters(1,GRAY)


        
def estDansPolygone(x,y,polygone):
    bool = True
    n = len(polygone)
    a = polygone[n-1][0] - x
    b = polygone[n-1][1] - y
    c = polygone[0][0] - polygone[n-1][0]
    d = polygone[0][1] - polygone[n-1][1]
    z = a*d - b*c
    if z < 0:
        s = -1
    elif z > 0:
        s = 1
    else :
        s = 0
    if s!=0:
        for i in (0, n-2):
            a = polygone[i][0] - x
            b = polygone[i][1] - y
            c = polygone[i+1][0] - polygone[i][0]
            d= polygone[i+1][1] - polygone[i][1]
            z = a*d - b*c
            if z == 0:
                break
            if z * s < 0:
                bool = False
                break
    return bool


def estDansCercle(Cercle, M):
    a = Cercle[0][0] - M[0]
    b = Cercle[0][1] - M[1]
    c=sqrt(a**2 + b**2)
    if c <= Cercle[1]:
        bool = True
    else:
        bool = False
    return bool

def estDansEnsembleCercles(ensemble,M):
    n = len(ensemble)
    bool = False
    for i in range(n-1):
        if estDansCercle(ensemble[i], M):
            bool = True
            break
    return bool

def setColorPlayerFromPosition(taches,player):
    fin=False
    color=GRAY
    i=0
    while not fin and i <len(taches):

        tache=taches[i][0]

        if estDansEnsembleCercles(tache,player.pos()):
            colore=True
            color=taches[i][1]
        i+=1
    player.colorbuff = color



########################################
###############ALGO 2 ##################
########################################
 
def randomPoints(n,size):
    """renvoie une liste de points tiré aléatoirement dans un rectangle de taile size"""
    lsPoints=[]
    h=size[1]
    w=size[0]
    for i in range(n):
        x=random.randint(0,w)
        y=random.randint(0,h)
        lsPoints+=[(x,y)]
    return lsPoints

def distPlusProche(p,pts):
    """Renvoie la distance entre le point p et le point le plus proche parmis les points"""
    points=pts[::]

    #on enleve p de la liste des points en cas de répétition
    if p in points:
        points.remove(p)
    #on initialise mini avec la distance au premier point de la liste des points
    mini=sqrt((p[0]-points[0][0])**2+(p[1]-points[0][1])**2)
    #on compare chaque point avec p pour trouver la plus petite distance
    for p2 in points:
        dist=sqrt((p2[0]-p[0])**2+(p2[1]-p[1])**2)
        if dist<mini:
            mini=dist

    return round(mini)


def randomHomogenePoints(n):
    """renvoie une liste de points qui sont répartis homogénement (a plus de 300px les uns des autres) mais aléatoirement """
    res=[]
    lsbase=[]
    for i in range(n):
        randomX= random.randint(0,SCREEN_WIDTH)
        randomY = random.randint(0,SCREEN_HEIGHT)
        if len(lsbase)>1:
            while distPlusProche((randomX,randomY),lsbase) < 300:
                randomX= random.randint(0,SCREEN_WIDTH)
                randomY = random.randint(0,SCREEN_HEIGHT)

        lsbase+=[(randomX,randomY)]
    return lsbase

def drawTache(screen,tache):
    #draw circles
    for cercle in tache[0]:
        centre=cercle[0]
        rayon=cercle[1]
        pygame.draw.circle(screen, tache[1], centre, rayon)




def createTache(taille):
    n= random.randint(taille[0],taille[1])
    lsCenters=randomPoints(n,(200,200))
    lsCircles=[]
    tot=(0,0)
    for c in lsCenters:
        rayon=distPlusProche(c,lsCenters)
        tot=(tot[0]+c[0],tot[1]+c[1])
        lsCircles+=[[c,rayon]]
    color=random.choice(COLORS)
    return [lsCircles,color]

def createNTaches(n,taille):
    lsTaches=[]
    #on créer les taches
    for i in range(n):
        lsTaches+=[createTache(taille)]
    #on créer une disposition aléatoire sur la map
    points=randomHomogenePoints(n)
    #on applique cette position a chaque tache
    for i in range(len(lsTaches)):
        tache=lsTaches[i][0]
        pos=points[i]
        for cercle in tache:
            cercle[0] =(cercle[0][0]+pos[0],cercle[0][1]+pos[1])
        lsTaches[i][0]=tache    

    return lsTaches

def drawAllTaches(screen,taches):
    for tache in taches:
        drawTache(screen,tache)