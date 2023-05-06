import random
import sys
import pygame

FPS = 60
WIDTH, HEIGHT = 900, 500
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
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
            Sweet(SWEET_WIDTH, SWEET_HEIGHT, (100, 200), 3, SWEET_IMAGE)
        ]
        pygame.display.set_caption("Sweets")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if random.randint(0, 150) == 1:
                self.sweets.append(
                    Sweet(SWEET_WIDTH, SWEET_HEIGHT, (random.randint(0, WIDTH - SWEET_WIDTH), -50), 3, SWEET_IMAGE
                          ))

            self.screen.blit(BACKGROUND_IMAGE, (0, 0))

            self.player.move(pygame.key.get_pressed())
            self.screen.blit(PLAYER_IMAGE, self.player.get_coordinates())

            for sweet in self.sweets:
                self.screen.blit(sweet.image, sweet.get_coordinates())

                if sweet.rect.colliderect(self.player.rect):
                    self.sweets.remove(sweet)

                sweet.fly()
                if sweet.get_coordinates()[1] > HEIGHT - sweet.rect.height:
                    self.sweets.remove(sweet)

            pygame.display.update()
            self.clock.tick(60)


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
