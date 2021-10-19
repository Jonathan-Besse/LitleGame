import pygame
import os
import random
pygame.init()

# GLOBAL CONSTANTS
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
RUNNING = [pygame.image.load(os.path.join("ressources/right-arrow.png")),
    pygame.image.load(os.path.join("ressources/right-arrow-2.png"))]
TP = [pygame.image.load(os.path.join("ressources/right-arrow_TP1.png")),
      pygame.image.load(os.path.join("ressources/right-arrow_TP2.png"))]
DOT = [pygame.image.load(os.path.join("ressources/record.png"))]
BG = pygame.image.load(os.path.join("ressources/Track.png"))





class Arrow():
    X_POS = 80
    Y_POS = 310
    TP_VEL = 8.5

    def __init__(self):
        self.tp_img = TP
        self.run_img = RUNNING
        self.arrow_run = True
        self.arrow_tp = False

        self.step_index = 0
        self.tp_vel = self.TP_VEL
        self.image = self.run_img[0]
        self.arrow_rect = self.image.get_rect()
        self.arrow_rect.x = self.X_POS
        self.arrow_rect.y = self.Y_POS

    def update(self, userInput):
        if self.arrow_run:
            self.run()
        if self.arrow_tp:
            self.tp()


        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_RIGHT] and not self.arrow_tp:
            self.arrow_tp = True
        elif not userInput[pygame.K_RIGHT]:
            self.arrow_tp = False
            self.arrow_run = True



    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.arrow_rect = self.image.get_rect()
        self.arrow_rect.x = self.X_POS
        self.arrow_rect.y = self.Y_POS
        self.step_index += 1

    def tp(self):
        self.image = self.tp_img[self.step_index // 10]
        self.arrow_rect = self.image.get_rect()
        self.arrow_rect.x = self.X_POS
        self.arrow_rect.y = self.Y_POS

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.arrow_rect.x, self.arrow_rect.y))


class Obstacle :
    def __init__(self, image, type):
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


class Dot(Obstacle):
    def __init__(self, image):
        # self.type = random.randint(0, 2)
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 325




def main():
    print("okk")

    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, run
    run = True
    clock = pygame.time.Clock()
    player = Arrow()
    game_speed = 14
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    font = pygame.font.Font('freesansbold.ttf', 20)
    death_count = 0

    def score() :
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Points : " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(Dot(DOT))
            elif random.randint(0, 2) == 1:
                obstacles.append(Dot(DOT))
            elif random.randint(0, 2) == 2:
                obstacles.append(Dot(DOT))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.arrow_rect.colliderect(obstacle.rect):
                i = death_count
                pygame.draw.rect(SCREEN, (255, 0, 0), player.arrow_rect, 2)
                pygame.time.delay(50)
                run = False
                menu(death_count=i+1)

        background()

        score()

        clock.tick(30)
        pygame.display.update()


def menu(death_count):
    global points
    on_menu = True
    while on_menu:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Appuie connard, j'ai pas que ça à foutre", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Appuie PUTAIN", True, (0, 0, 0))
            score = font.render("VOILA TON PUTAIN DE SCORE DE MERDE !!!!", True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on_menu = False
            if event.type == pygame.KEYDOWN:
                on_menu = False
                main()


menu(death_count=0)