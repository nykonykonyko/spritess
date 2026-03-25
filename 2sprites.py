import pygame, pyautogui, random

pygame.init()
WIDTH, HEIGHT = pyautogui.size()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Projcontrol")

hueco   = pygame.transform.scale(pygame.image.load("hueco.jpg"),  (WIDTH, HEIGHT))
primera = pygame.transform.scale(pygame.image.load("starrk.png"), (150, 200))
dark    = pygame.transform.scale(pygame.image.load("darkk.png"),  (150, 200))

clock     = pygame.time.Clock()
lastenemy = pygame.time.get_ticks() - 1500

# ── Bullet ────────────────────────────────────────────────────────────────────
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 8), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 220, 50), (0, 0, 20, 8), border_radius=3)
        self.rect  = self.image.get_rect()
        self.rect.midleft = (x, y)   # spawn at player's right edge, vertically centred

    def movement(self):
        self.rect.x += 15            # flies to the right
        if self.rect.left > WIDTH:   # off-screen — remove it
            self.kill()

# ── Enemy ─────────────────────────────────────────────────────────────────────
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = dark
        self.rect  = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(50, HEIGHT - 50)

    def movement(self):
        self.rect.x -= 10
        if self.rect.right < 0:
            self.kill()

# ── Player ────────────────────────────────────────────────────────────────────
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = primera
        self.rect  = self.image.get_rect()
        self.rect.topleft = (50, HEIGHT // 2)
        self.shoot_cooldown = 0      # frames until next shot is allowed

    def movement(self, keys):
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -10)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, 10)

    def shoot(self, bulletgroup):
        """Fire one bullet from the player's right edge."""
        if self.shoot_cooldown == 0:
            bullet = Bullet(self.rect.right, self.rect.centery)
            bulletgroup.add(bullet)
            self.shoot_cooldown = 15  # ~0.25 s at 60 FPS — tweak to taste

    def update_cooldown(self):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

# ── Groups ────────────────────────────────────────────────────────────────────
enemygroup  = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
spritegroup = pygame.sprite.Group()

p = Player()
spritegroup.add(p)

# ── Main loop ─────────────────────────────────────────────────────────────────
while True:
    # Events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()

    # Input
    pressedkeys = pygame.key.get_pressed()
    p.movement(pressedkeys)

    if pressedkeys[pygame.K_SPACE]:
        p.shoot(bulletgroup)

    p.update_cooldown()

    # Spawn enemies
    timenow = pygame.time.get_ticks()
    if timenow - lastenemy > 1500:
        enemygroup.add(Enemy())
        lastenemy = timenow

    # Move everything
    for enemy in enemygroup:
        enemy.movement()

    for bullet in bulletgroup:
        bullet.movement()

    # Bullet ↔ enemy collision — True = kill the bullet on hit too
    pygame.sprite.groupcollide(bulletgroup, enemygroup, True, True)

    # Draw
    screen.blit(hueco, (0, 0))
    spritegroup.draw(screen)
    enemygroup.draw(screen)
    bulletgroup.draw(screen)

    pygame.display.update()
    clock.tick(60)
