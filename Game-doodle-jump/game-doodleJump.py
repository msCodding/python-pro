import pygame
from random import randint as r, choice

w, h = 400, 550
fps = 60
gravity = 1
max_platforms = 10
scroll_h = 200
scroll = 0
bg_scroll = 0
game_over = False

clock = pygame.time.Clock()
pygame.init()  # возможность пользоваться библиотекой
# инициализация окна
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption('Дудл джамп')
# указание названия вашего окна
bg_image = pygame.image.load('image/Background_paper.png')
bg_image = pygame.transform.scale(bg_image, (w, h))


class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(center=(x, y))
        self.flip = False

    def show(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False),
                    (self.rect.x, self.rect.y))


class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'image/player.png', 60, 60)
        self.speed = 10
        self.flip = False
        self.velocity_y = 0

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_a]:
            if self.rect.right < 0: self.rect.left = w
            self.rect.x -= self.speed
            self.flip = False
        if key[pygame.K_d]:
            if self.rect.left > w: self.rect.right = 0
            self.rect.x += self.speed
            self.flip = True
        self.velocity_y += gravity
        self.rect.y += self.velocity_y
        # если коснулся нижней границей пола оттолкнуться -20
        # if self.rect.bottom > h:
        #     self.rect.bottom = h
        #     self.velocity_y = -20
        for p in platform_group:
            if p.rect.colliderect(self.rect):
                if self.rect.bottom < p.rect.bottom:
                    if self.velocity_y > 0:
                        self.rect.bottom = p.rect.top
                        self.velocity_y = -20
        scroll = 0
        if self.rect.top <= scroll_h:
            scroll = 5
        return scroll


class Platform(GameObject):
    def __init__(self, x, y,type = 'static'):
        super().__init__(x, y, 'image/platform_static.png', 100, 20)
        self.type = type
        self.speed = r(1,5)

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > h:
            self.kill()
        if self.type == 'moving':
            self.rect.x += self.speed
            if self.rect.right > w or self.rect.left <0:
                self.speed *= -1
        if self.type == 'broke':
            self.image.set_alpha(80)




pl = Player(w // 2, h // 2 + 150)
platform = Platform(w // 2, h - 50)
platform_group = pygame.sprite.Group()
platform_group.add(platform)


def showText(label, x, y,size=60,font='game_over_TagType.ttf',color=(255, 0, 0)):
    f1 = pygame.font.Font(font, size)
    text = f1.render(label, True, color)
    screen.blit(text, (x, y))


run = True
while run:
    if not game_over:
        if bg_scroll >= h:
            bg_scroll = 0
        screen.blit(bg_image, (0, bg_scroll))
        screen.blit(bg_image, (0, bg_scroll - h))
        bg_scroll += scroll
        if len(platform_group) < max_platforms:
            x = r(100, w - 100)
            y = platform.rect.y - r(130, h - 130)
            type = choice(['static','moving','broke'])
            plat = Platform(x, y,type)
            platform_group.add(plat)
        platform_group.draw(screen)
        platform_group.update(scroll)
        pl.show()
        scroll = pl.move()
        if pl.rect.top > h: game_over = True
        platform.show()
    else:
        showText('Game over',w//2-100,h//2-100)
        showText('Нажмите пробел чтобы начать заново',
                 w//2-150,
                 h//2,
                 20,
                 'ofont.ru_Buira.ttf',
                 (100, 100, 100))


    pygame.display.flip()
    # обновление отрисовки на экране
    for i in pygame.event.get():
        if i.type == pygame.QUIT: run = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:
                game_over = False
                scroll = 0
                pl = Player(w // 2, h // 2 + 150)
                platform_group.empty()
                platform = Platform(w // 2, h - 50)
                platform_group.add(platform)

    clock.tick(fps)
