import pygame
import os
import random

pygame.init()

#Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")), pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")), pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]


LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")), 
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))

BACKGROUND = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

#Global Variables
game_speed = 0
x_pos_bg = 0
y_pos_bg = 0
points = 0

obstacles = []

dinosaurs = []

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_DUCK_POS = 340
    JUMP_VEL = 8.5

    def __init__(self) -> None:
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING


        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()

        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
    

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()

        if self.step_index >= 20:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False

        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        
        elif not(self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False


    def duck(self):
        self.image = self.duck_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_DUCK_POS
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 10]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 3
            self.jump_vel -= 0.6
        
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL


    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self) -> None:
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(800, 1000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
         SCREEN.blit(self.image, (self.x, self.y))


class Obstacle:
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH


    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()


    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325



class LargeCactus(Obstacle):
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300



class Bird(Obstacle):
    def __init__(self, image) -> None:
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(120, 320)
        self.index = 0
    

    def draw(self, SCREEN):
        if self.index >= 19:
            self.index = 0
        
        SCREEN.blit(self.image[self.index // 10], self.rect)
        self.index += 1


def remove(index):
    dinosaurs.pop(index)

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs
    
    run = True
    clock = pygame.time.Clock()

    dinosaurs = [Dinosaur()]

    cloud = Cloud()
    
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)


    def update_score():
        global points, game_speed
        points += 1
        if points % 200 == 0:
            game_speed += 1
        
        text = font.render("Points: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)


    def update_background():
        global x_pos_bg, y_pos_bg, game_speed
        image_width = BACKGROUND.get_width()
        SCREEN.blit(BACKGROUND, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))

        if x_pos_bg <= -image_width:
            SCREEN.blit(BACKGROUND, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()


        if len(dinosaurs) == 0:
            break

        for dinosaur in dinosaurs:
            dinosaur.draw(SCREEN)
            dinosaur.update(userInput)

        if len(obstacles) == 0:
            temp = random.randint(0, 100)
            if temp == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif temp == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif temp == 2:
                obstacles.append(Bird(BIRD))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.dino_rect.colliderect(obstacle.rect):
                    remove(i)

        update_background()

        cloud.draw(SCREEN)
        cloud.update()

        update_score()

        clock.tick(60)
        pygame.display.update()

main()