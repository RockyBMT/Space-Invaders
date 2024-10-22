import pygame
import random
pygame.init()

clock = pygame.time.Clock()
tim=0
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)

font = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 40)
text = font.render("SCORE: 000000",True,WHITE)

size=(700,700)
screen=pygame.display.set_mode(size)
pygame.display.set_caption("Space Invaders")
done = False

direction = "right"
change=0
select=0

score=0
minus=0
lives=3
tim2=0
obstacle_positions = [(100, 600), (300, 600), (500, 600)]

sound1 = pygame.mixer.Sound("shoot.wav")
sound2 = pygame.mixer.Sound("invaderkilled.wav")

class Character(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png").convert()
        self.image.set_colorkey(WHITE)
        self.color=(WHITE)

        self.sizex=30
        self.sizey=30
        self.x=100
        self.y=670

        self.x_speed = 0
        self.y_speed = 0

        self.rect = self.image.get_rect()

    def move(self):
        self.x+=self.x_speed
        self.y+=self.y_speed
    def draw (self, screen):
        #pygame.draw.rect(screen, self.color,[self.x, self.y, self.sizex,self.sizey], 0)
        screen.blit(self.image,(self.x,self.y))
        self.rect=pygame.Rect(self.x,self.y,60,30)
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color=WHITE
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.y=680
        self.rect.x=character1.x + 27.5
        self.x=character1.x + 14

    def update(self):
        self.rect.y+=-12
        screen.blit(self.image,(self.rect))
        if self.rect.y <-10:
            self.kill()
        #pygame.draw.rect(screen, self.color,[self.x, self.y, self.sizex,self.sizey], 0)
class Bulletenemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        global select
        self.image = pygame.Surface([5, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y+=3
        screen.blit(self.image,(self.rect))
        if self.rect.y >707:
            self.kill()
class Enemy(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image = pygame.image.load("red.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rectmax = pygame.Rect(x+40,y+32,40,32)
    
    def update(self):
        global direction
        if direction == "right":
            self.rect.x+=1
        else:
            self.rect.x+=-1

        for bullet in bullet_group:
            #if bullet.rect >= self.rect and bullet.rect <= self.rectmax:
            if pygame.sprite.spritecollide(bullet, enemy_group,True):
                #self.kill()
                bullet.kill()
                global score
                score+=1
                sound2.play()
        screen.blit(self.image,(self.rect))
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([100, 30])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = 5

    def damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
        elif self.health ==3 or self.health ==2:
            self.image.fill((200, 200, 200))
        elif self.health <= 1:
            self.image.fill((100,100,100))
class SpecialEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("extra.png").convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = -50
        self.rect.y = 50 
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()

special_enemy_group = pygame.sprite.Group()
special_enemy_timer = 0
bgimg=pygame.image.load("spaceinvadebackground.png").convert()
bgimg = pygame.transform.scale(bgimg, (700, 700)) 

def spawn_special_enemy():
    special_enemy = SpecialEnemy()
    special_enemy_group.add(special_enemy)

character1 = Character()
bullet2_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
for pos in obstacle_positions:
    obstacle = Obstacle(pos[0], pos[1])
    obstacle_group.add(obstacle)

for row in range(5):
    for col in range(10):
        enemy = Enemy(x=col * 60 + 50, y=row * 50 + 50)
        enemy_group.add(enemy)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done= True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                character1.x_speed = 3
            elif event.key == pygame.K_LEFT:
                character1.x_speed =-3
            elif event.key == pygame.K_SPACE:
                if tim2>=30:
                    bullet=Bullet()
                    bullet_group.add(bullet)
                    tim2=0
                    sound1.play()
        elif event.type == pygame.KEYUP:
            if (event.key == pygame.K_RIGHT and character1.x_speed == 3) or (event.key == pygame.K_LEFT and character1.x_speed == -3):
                character1.x_speed = 0
    tim+=1
    for bullet in bullet_group:
        obstacle_hit_list = pygame.sprite.spritecollide(bullet, obstacle_group, False)
        if obstacle_hit_list:
            bullet.kill()
            for obstacle in obstacle_hit_list:
                obstacle.damage()
    for bullet2 in bullet2_group:
        obstacle_hit_list = pygame.sprite.spritecollide(bullet2, obstacle_group, False)
        if obstacle_hit_list:
            bullet2.kill()
            for obstacle in obstacle_hit_list:
                obstacle.damage()
    special_enemy_timer += 1
    if special_enemy_timer > random.randint(500, 1000):
        spawn_special_enemy()
        special_enemy_timer = 0
    special_enemy_group.update()
    for bullet in bullet_group:
        if pygame.sprite.spritecollide(bullet, special_enemy_group, True):
            bullet.kill()
            score += 10
            sound2.play()
    if tim == 80-minus:
        try:
            enemy = random.choice(enemy_group.sprites())
            bullet_enemy = Bulletenemy(enemy.rect.x+19, enemy.rect.y+32)
            bullet2_group.add(bullet_enemy)
            tim=0
        except:
            for row in range(5):
                for col in range(10):
                    enemy = Enemy(x=col * 60 + 50, y=row * 50 + 50)
                    enemy_group.add(enemy)
            tim=0
            minus+=20
    for enemy in enemy_group:
        if enemy.rect.x >= 660:
            direction = "left"
            for enemy in enemy_group:
                enemy.rect.y+=10
            break
        elif enemy.rect.x == 0:
            direction = "right"
            for enemy in enemy_group:
                enemy.rect.y+=10
            break
        if enemy.rect.y >= 700:
            lives=0
    tim2+=1
    screen.fill(BLACK)
    screen.blit(bgimg, [0, 0, 700,700])
    special_enemy_group.draw(screen)
    obstacle_group.draw(screen)
    obstacle_group.update()
    bullet_group.update()
    enemy_group.update()
    bullet2_group.update()
    character1.move()
    character1.draw(screen)
    text = font.render("SCORE: "+str(score),True,WHITE)
    screen.blit(text, [5,0])
    text2 = font.render("LIVES: "+str(lives),True,WHITE)
    screen.blit(text2,[546,0])
    if pygame.sprite.spritecollide(character1, bullet2_group,True):
        lives+=-1
    if lives ==0:
        enemy_group.empty()
        score=0
        lives=3
        tim=0
        screen.fill(RED)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()