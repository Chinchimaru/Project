import pygame
from os import path
import random
import time
img_dir = path.join(path.dirname("__file__"), 'img')
snd_dir = path.join(path.dirname("__file__"), 'snd')
pygame.init()
pygame.mixer.init()
WIDTH = 990
HEIGHT = 1020
FPS = 60
WHITE = (255, 255, 255)
gem1 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "1.png")), (30, 30))
gem2 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "2.png")), (30, 30))
gem3 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "3.png")), (30, 30))
gem4 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "4.png")), (30, 30))
gem5 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "5.png")), (30, 30))
gem6 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "6.png")), (30, 30))
ocm = pygame.image.load(path.join(img_dir, "player.png"))
life = pygame.image.load(path.join(img_dir, "life.png"))
dead = pygame.image.load(path.join(img_dir, "dead.png"))
meteor1 = pygame.image.load(path.join(img_dir, "meteor1.png"))
meteor2 = pygame.image.load(path.join(img_dir, "meteor2.png"))
star1 = pygame.transform.scale(pygame.image.load(path.join(img_dir, "star1.png")), (30, 30))
GREEN = [gem1, gem2, gem3, gem4, gem5, gem6]
RED = [meteor1, meteor2]
BLUE = [star1]
background = pygame.transform.scale(pygame.image.load(path.join(img_dir, "back.png")), (WIDTH, HEIGHT))
background_rect = background.get_rect()
eat = [BLUE, RED, RED, RED, RED, GREEN, GREEN, GREEN, GREEN, GREEN]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Накорми чела")
clock = pygame.time.Clock()
preview = pygame.mixer.Sound(path.join(snd_dir, 'preview.wav'))
music = pygame.mixer.Sound(path.join(snd_dir, 'music.wav'))
damage = pygame.mixer.Sound(path.join(snd_dir, 'damage.wav'))
gem = pygame.mixer.Sound(path.join(snd_dir, 'gem.wav'))
star = pygame.mixer.Sound(path.join(snd_dir, 'star.wav'))
miss = pygame.mixer.Sound(path.join(snd_dir, 'miss.wav'))
cluck = pygame.mixer.Sound(path.join(snd_dir, 'menu.wav'))
loss = pygame.mixer.Sound(path.join(snd_dir, 'loss.wav'))


def end_game(text, size, y, sound):
    afk_time = pygame.time.get_ticks()
    music.stop()
    sound.play()
    screen.blit(background, background_rect)
    draw_text(text, size, y)
    pygame.display.flip()
    while pygame.time.get_ticks() - afk_time < 4000:
        pass
    sound.stop()


def draw_text(text, size, y, x=WIDTH / 2):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def menu():  # главное меню с возможностью начать игру занова или выйти
    music.stop()
    preview.play(-1)
    screen.blit(background, background_rect)
    draw_text("НАКОРМИ ЧЕЛА", 90, 190)
    draw_text("НАЧАТЬ", 100, 490)
    draw_text("ВЫЙТИ", 100, 640)
    pygame.display.flip()
    wait = True
    while wait:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return False
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if (590 >= ev.pos[1] >= 490) and (WIDTH / 2 + 160 >= ev.pos[0] >= WIDTH / 2 - 160):
                        preview.stop()
                        wait = False
                        return True
                    if (740 >= ev.pos[1] >= 640) and (WIDTH / 2 + 145 >= ev.pos[0] >= WIDTH / 2 - 145):
                        pygame.quit()
                        return False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ocm
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT
        self.speedx = 0
        self.hp = 0
        self.take = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -15
        if keystate[pygame.K_d]:
            self.speedx = 15
        self.rect.x += self.speedx
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        self.rect.x += self.speedx


class Hp(pygame.sprite.Sprite):
    def __init__(self, d, state=life):
        pygame.sprite.Sprite.__init__(self)
        self.image = state
        self.rect = self.image.get_rect()
        self.rect.right = WIDTH - 10
        self.rect.y = d


class Mob(pygame.sprite.Sprite):
    def __init__(self, r):
        pygame.sprite.Sprite.__init__(self)
        self.nps = random.choice(eat)
        self.eat = random.choice(self.nps)
        self.image = self.eat
        self.rect = self.image.get_rect()
        self.rect.centerx = r
        self.rect.bottom = 0
        self.speedy = random.randint(2, 5)

    def update(self):
        if self.rect.top > HEIGHT:
            if self.nps == GREEN:
                if player.hp <= 4:
                    miss.play()
                    hp_list[player.hp].kill()
                    hp_list[player.hp] = Hp(player.hp * 50, dead)
                    all_sprites.add(hp_list[player.hp])
                    player.hp += 1
            self.rect.bottom = 0
            self.speedy = random.randint(2, 5)
            self.nps = random.choice(eat)
            self.eat = random.choice(self.nps)
            self.image = self.eat
        self.rect.y += self.speedy


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
play = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
play.add(player)
mob = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in range(10):
    mob[i] = Mob(i * 100 + 15)
    all_sprites.add(mob[i])
    mobs.add(mob[i])
hp_list = [0, 1, 2, 3, 4]
for i in range(5):
    hp_list[i] = Hp(i * 50)
    all_sprites.add(hp_list[i])
game = True
game_over = True
while game:
    if game_over:
        for i in range(10):
            mob[i].nps = random.choice(eat)
            mob[i].eat = random.choice(mob[i].nps)
            mob[i].image = mob[i].eat
            mob[i].rect.bottom = 0
        player.hp = 0
        player.take = 0
        player.rect.centerx = WIDTH / 2
        for i in range(5):
            hp_list[i].kill()
            hp_list[i] = Hp(i * 50)
            all_sprites.add(hp_list[i])
        menu()
        music.play(-1)
        game_over = False
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    for k in range(10):
        hit = pygame.sprite.spritecollide(mob[k], play, False)
        if hit:
            if mob[k].nps == RED:
                if player.hp <= 4:
                    damage.play()
                    hp_list[player.hp].kill()
                    hp_list[player.hp] = Hp(player.hp * 50, dead)
                    all_sprites.add(hp_list[player.hp])
                    player.hp += 1
            if mob[k].nps == GREEN:
                gem.play()
                player.take += 1
            if mob[k].nps == BLUE:
                if player.hp - 1 >= 0:
                    star.play()
                    player.hp -= 1
                    hp_list[player.hp].kill()
                    hp_list[player.hp] = Hp(player.hp * 50, life)
                    all_sprites.add(hp_list[player.hp])
            mob[k].rect.bottom = 0
            mob[k].speedy = random.randint(1, 7)
            mob[k].nps = random.choice(eat)
            mob[k].eat = random.choice(mob[k].nps)
            mob[k].image = mob[k].eat
    if player.take >= 40:
        end_game("ВЫ ПОБЕДИЛИ !", 10, HEIGHT / 2 - 50, loss)
        game_over = True
    if player.hp > 4:
        end_game("ВЫ ПРОИГРАЛИ ((((", 10, HEIGHT / 2 - 50, loss)
        game_over = True
    all_sprites.update()
    screen.blit(background, background_rect)
    draw_text(str(player.take), 40, 100)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
