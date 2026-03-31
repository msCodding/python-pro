import pygame

w,h = 400,550
fps = 60


clock = pygame.time.Clock()
pygame.init() # возможность пользоваться библиотекой
            # инициализация окна
screen = pygame.display.set_mode((w,h))
pygame.display.set_caption('Дудл джамп')
# указание названия вашего окна
bg_image = pygame.image.load('image/Background_paper.png')
bg_image = pygame.transform.scale(bg_image,(w,h))

class GameObject(pygame.sprite.Sprite):
    def __init__(self,x,y,image,w,h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image,(w,h))
        self.rect = self.image.get_rect(center = (x,y))
    def show(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))
class Player(GameObject):
    def __init__(self,x,y):
        super().__init__(x,y,'image/player.png',60,60)
pl = Player(w//2,h//2+150)
run = True
while run:
    screen.blit(bg_image,(0,0))
    pl.show()
    pygame.display.flip()
    # обновление отрисовки на экране
    for i in pygame.event.get():
        if i.type == pygame.QUIT:run=False
    clock.tick(fps)

