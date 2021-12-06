import pygame
import os
import random
import numpy as np
import sys
import math
#Global Constants

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100

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
# global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs, dinosaurs_copy

game_speed = 0
x_pos_bg = 0
y_pos_bg = 0
points = 0

obstacles = []

dinosaurs = []

dinosaurs_copy = []

class NeuralNet:
    def __init__(self) -> None:
        self.Theta1 = (np.random.randn(3, 3) * 2 * 0.12 - 0.12)
        self.Theta2 = (np.random.randn(3, 4) * 2 * 0.12 - 0.12)
    
    def display(self):
        print(self.Theta1)
        print(self.Theta2)


class Dinosaur(NeuralNet):
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

        self.score = 0

        super().__init__()
    

    def update(self, move):
        if self.dino_duck:
            self.duck()
        if self.dino_jump:
            self.jump()
        if self.dino_run:
            self.run()

        if self.step_index >= 20:
            self.step_index = 0

        if np.argmax(move) == 0 and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False
            self.dino_duck = False

        elif np.argmax(move) == 1 and not self.dino_jump:
            self.dino_duck = True
            self.dino_jump = False
            self.dino_run = False
        
        elif not(self.dino_jump or np.argmax(move) == 1):
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

def game():
    pygame.init()
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, dinosaurs, dinosaurs_copy
    
    run = True
    clock = pygame.time.Clock()

    dinosaurs_copy = dinosaurs.copy()
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

    def distance(pos_a, pos_b):
        dx = pos_a[0] - pos_b[0]
        dy = pos_a[1] - pos_b[1]
        return math.sqrt(dx**2 + dy**2)


    def get_output(inputs: np.matrix):
        def sigmoid(x: np.matrix):
            return(1 / (1 + np.exp(-x)))
        a1 = inputs.transpose()
        a1 = np.insert(a1, 0, 1, axis=0)
        z2 = np.dot(dinosaur.Theta1, a1)
        a2 = sigmoid(z2)
        a2 = np.insert(a2, 0, 1, axis=0)
        z3 = np.dot(dinosaur.Theta2, a2)
        a3 = sigmoid(z3)
        return a3

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        SCREEN.fill((255, 255, 255))
        # userInput = pygame.key.get_pressed()

        moves = []
        
        if len(dinosaurs) == 0:
            pygame.quit()
            obstacles.pop()
            break


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
                    dinosaur.score = points
                    remove(i)

        for dinosaur in dinosaurs:
            if len(obstacles) == 0:
                dist = distance((dinosaur.dino_rect.x, dinosaur.dino_rect.y), [10000, 310])
            else:
                dist = distance((dinosaur.dino_rect.x, dinosaur.dino_rect.y), obstacles[0].rect.midtop)
            moves.append(get_output(np.matrix([dinosaur.dino_rect.y, dist], dtype=np.float64)))

        for i, dinosaur in enumerate(dinosaurs):
            dinosaur.draw(SCREEN)
            dinosaur.update(moves[i])
        
        update_background()

        cloud.draw(SCREEN)
        cloud.update()

        update_score()

        clock.tick(60)
        pygame.display.update()


def Dino_compare(dino_obj: Dinosaur):
    return dino_obj.score

def updateNet():
    dinosaurs_copy.sort(key=Dino_compare, reverse=True)
    limit = 7
    for i in range(limit - 1):
        for j in range(i + 1, limit):
            temp_dino = Dinosaur()
            for row in range(temp_dino.Theta1.shape[0]):
                for col in range(temp_dino.Theta1.shape[1]):
                    temp_dino.Theta1[row][col] = (dinosaurs_copy[i].Theta1[row][col] + dinosaurs_copy[j].Theta1[row][col]) / 2
            
            for row in range(temp_dino.Theta2.shape[0]):
                for col in range(temp_dino.Theta2.shape[1]):
                    temp_dino.Theta2[row][col] = (dinosaurs_copy[i].Theta2[row][col] + dinosaurs_copy[j].Theta2[row][col]) / 2
            dinosaurs.append(temp_dino)      

for iters in range(10):
    if iters == 0:
        for i in range(21):
            dinosaurs.append(Dinosaur())
    game()
    updateNet()