import random
import sys
import pygame

FPS = 60
WIDTH, HEIGHT = 900, 500
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
HEART_WIDTH, HEART_HEIGHT = 50, 50
SWEET_WIDTH, SWEET_HEIGHT = 70, 70
BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("fon.jpg"), (WIDTH, HEIGHT)
)
PLAYER_IMAGE = pygame.transform.scale(
    pygame.image.load("player.png"), (PLAYER_WIDTH, PLAYER_HEIGHT)
)
SWEET_IMAGE = pygame.transform.scale(
    pygame.image.load("candy.png"), (SWEET_WIDTH, SWEET_HEIGHT)
)
SWEET2_IMAGE = pygame.transform.scale(
    pygame.image.load("candy2.png"), (SWEET_WIDTH, SWEET_HEIGHT)
)
POISON_IMAGE = pygame.transform.scale(
    pygame.image.load("poison.png"), (SWEET_WIDTH, SWEET_HEIGHT)
)
SPEED_IMAGE = pygame.transform.scale(
    pygame.image.load("speedcandy.png"), (SWEET_WIDTH, SWEET_HEIGHT)
)
HEART_IMAGE = pygame.transform.scale(
    pygame.image.load("life.png"), (HEART_WIDTH, HEART_HEIGHT)
)

class Sprite:
    def __init__(self, width, height, start_coordinates, speed, image):
        self.width = width
        self.height = height
        self.start_coordinates = start_coordinates
        self.speed = speed
        self.image = image

        self.rect = pygame.rect.Rect(*start_coordinates, width, height)

    def change_coordinates(self, x=0, y=0):
        self.rect.x += x
        self.rect.y += y

    def set_coordinates(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def get_coordinates(self):
        return self.rect.x, self.rect.y


class Player(Sprite):
    def __init__(self, width, height, start_coordinates, speed, image):
        super().__init__(width, height, start_coordinates, speed, image)

    def move(self, pressed):
        if pressed[pygame.K_a] and self.rect.x > 0:
            self.change_coordinates(x=-self.speed)
        if pressed[pygame.K_d] and self.rect.x < WIDTH - self.width:
            self.change_coordinates(x=self.speed)

    def fall(self):
        pass


class Sweet(Sprite):
    def __init__(self, width, height, start_coordinates, speed, image):
        super().__init__(width, height, start_coordinates, speed, image)

    def fly(self):
        self.change_coordinates(y=self.speed)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.player = Player(PLAYER_WIDTH, PLAYER_HEIGHT, (400, 250), 4, PLAYER_IMAGE)
        self.sweets = [
            Sweet(SWEET_WIDTH, SWEET_HEIGHT, (100, 200), 3, SWEET_IMAGE),
            Sweet(SWEET_WIDTH, SWEET_HEIGHT, (200, 100), 3, SWEET2_IMAGE),
            Sweet(SWEET_WIDTH, SWEET_HEIGHT, (20, 100), 3, POISON_IMAGE),
            Sweet(SWEET_WIDTH, SWEET_HEIGHT, (200, 10), 3, SPEED_IMAGE)
        ]
        self.poison = Sweet(SWEET_WIDTH, SWEET_HEIGHT, (200, 10), 3, POISON_IMAGE)
        self.candspeed = Sweet(SWEET_WIDTH, SWEET_HEIGHT, (200, 10), 3, SPEED_IMAGE)
        self.hearts = 5
        pygame.display.set_caption("Sweets")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.hearts <= 0:
                    pygame.quit()
                    sys.exit()

            if random.randint(0, 500) == 1:
                self.sweets.append(
                    Sweet(SWEET_WIDTH, SWEET_HEIGHT, (random.randint(0, WIDTH - SWEET_WIDTH), -50), 3, SWEET_IMAGE))
                self.sweets.append(
                    Sweet(SWEET_WIDTH, SWEET_HEIGHT, (random.randint(0, WIDTH - SWEET_WIDTH), 0), 3, SWEET2_IMAGE))
            if random.randint(0, 1000) == 1:
                self.sweets.append(
                    Sweet(SWEET_WIDTH, SWEET_HEIGHT, (random.randint(0, WIDTH - SWEET_WIDTH), 0), 3, POISON_IMAGE))
                self.sweets.append(
                    Sweet(SWEET_WIDTH, SWEET_HEIGHT, (random.randint(0, WIDTH - SWEET_WIDTH), 1), 3, SPEED_IMAGE))

            self.screen.blit(BACKGROUND_IMAGE, (0, 0))
            for i in range(self.hearts):
                self.screen.blit(HEART_IMAGE, (10 + i * 50, 10))

            self.player.move(pygame.key.get_pressed())
            self.screen.blit(PLAYER_IMAGE, self.player.get_coordinates())

            for sweet in self.sweets:
                self.screen.blit(sweet.image, sweet.get_coordinates())

                if self.candspeed.rect.colliderect(self.player.rect):
                    self.speed += 1

                if self.poison.rect.colliderect(self.player.rect):
                    self.speed -= 1


                if sweet.rect.colliderect(self.player.rect):
                    self.sweets.remove(sweet)
                    if self.hearts < 5:
                        self.hearts += 1


                sweet.fly()
                if sweet.get_coordinates()[1] > HEIGHT - sweet.rect.height:
                    self.sweets.remove(sweet)
                    self.hearts -= 1
            pygame.display.update()
            self.clock.tick(60)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
