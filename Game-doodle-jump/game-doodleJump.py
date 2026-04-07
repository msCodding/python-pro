import pygame
from random import randint as r

w, h = 400, 550
fps = 60
gravity = 1
max_platforms = 10
scroll_h = 200
scroll = 0

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
        if self.rect.bottom > h:
            self.rect.bottom = h
            self.velocity_y = -20
        for p in platform_group:
            if p.rect.colliderect(self.rect):
                if self.rect.bottom<p.rect.bottom:
                    if self.velocity_y > 0:
                        self.rect.bottom = p.rect.top
                        self.velocity_y =-20
        scroll = 0
        if self.rect.top <= scroll_h:
            scroll = 5
        return scroll


class Platform(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 'image/platform_static.png', 100, 20)
    def update(self,scroll):
        self.rect.y += scroll

pl = Player(w // 2, h // 2 + 150)
platform = Platform(w // 2, h - 50)
platform_group = pygame.sprite.Group()
for i in range(max_platforms):
    x, y = r(100, w-100), r(130, h-130)
    platform_group.add(Platform(x, y))

run = True
while run:
    screen.blit(bg_image, (0, 0))
    platform_group.draw(screen)
    platform_group.update(scroll)
    pl.show()
    scroll=pl.move()
    platform.show()

    pygame.display.flip()
    # обновление отрисовки на экране
    for i in pygame.event.get():
        if i.type == pygame.QUIT: run = False
    clock.tick(fps)
