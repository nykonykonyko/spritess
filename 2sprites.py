import pygame, pyautogui, random
pygame.init()
WIDTH,HEIGHT = pyautogui.size()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Projcontrol")
hueco = pygame.transform.scale(pygame.image.load("hueco.jpg"),(WIDTH,HEIGHT))
primera = pygame.transform.scale(pygame.image.load("starrk.png"),(150,200))
dark = pygame.transform.scale(pygame.image.load("darkk.png"),(150,200))
clock = pygame.time.Clock()
lastenemy = pygame.time.get_ticks() - 1500
lives = 10


class Enemy(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = dark

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(50,HEIGHT-50)

    def movement(self):
        self.rect.x -= 10
        if self.rect.right < 0 :
            self.kill()
enemygroup = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = primera

        self.rect = self.image.get_rect()
    def movement(self,keys):
        if keys[pygame.K_UP]:
            self.rect.move_ip(0,-10)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0,10)    
spritegroup = pygame.sprite.Group()
p = Player() 

spritegroup.add(p)
while True:
    screen.blit(pygame.image.load("hueco.jpg"),(0,0))
    for e in pygame.event.get():

            if e.type == pygame.QUIT:
                pygame.quit()
    pressedkeys = pygame.key.get_pressed()

    p.movement(pressedkeys)
    spritegroup.draw(screen)
    if len(enemygroup) > 0 :
        pass
    timenow = pygame.time.get_ticks()
    if timenow - lastenemy > 1500 :
        E = Enemy()
        enemygroup.add(E)
        print(E)
        lastenemy = timenow
    enemygroup.draw(screen)
    for e in enemygroup:
         e.movement()
    if pygame.sprite.groupcollide(spritegroup,enemygroup,False,True):
        lives-=1
        print(lives)
    #if spritegroup :
       
    pygame.display.update()
