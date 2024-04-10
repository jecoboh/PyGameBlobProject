import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SPACE_SIZE = 50

game_over = 0
main_menu = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Blob')

# Images

sky_img = pygame.image.load('C:/Users/juane/Images/GameImages/sky.jpg')
game_over_image = pygame.image.load('C:/Users/juane/Images/GameImages/restart.png')
start_image = pygame.image.load('C:/Users/juane/Images/GameImages/start.png')
win_image = pygame.image.load('C:/Users/juane/Images/GameImages/win.jpg')


class Win:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (SPACE_SIZE * 6, SPACE_SIZE * 3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)


class Button:
    def __init__(self, x, y, image):
        self.image = pygame.transform.scale(image, (SPACE_SIZE * 6.5, SPACE_SIZE * 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        mouse_position = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action


class Player:
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):

        dx = 0
        dy = 0

        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jump and not self.in_air:
                self.vel_y = -18.2
                self.jump = True
            if not key[pygame.K_SPACE]:
                self.jump = False
            if key[pygame.K_LEFT]:
                dx -= 3
            if key[pygame.K_RIGHT]:
                dx += 3

            # Gravity
            self.vel_y += 1
            if self.vel_y > 15:
                self.vel_y = 15
            dy += self.vel_y


            # Check for collision
            self.in_air = True
            for space in world.space_list:
                # check for collision in x direction
                if space[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # check for collision in y direction
                if space[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # check if bellow the ground = jumping
                    if self.vel_y < 0:
                        dy = space[1].bottom - self.rect.top
                        self.vel_y = 0
                    # check if above the ground = falling
                    elif self.vel_y >= 0:
                        dy = space[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, enemy_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, door_group, False):
                game_over = 1

            self.rect.x += dx
            self.rect.y += dy


        screen.blit(self.player, self.rect)
        # pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)

        return game_over

    def reset(self, x, y):
        image = pygame.image.load('C:/Users/juane/Images/GameImages/character.jpg')
        self.player = pygame.transform.scale(image, (SPACE_SIZE, SPACE_SIZE))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.player.get_width()
        self.height = self.player.get_height()
        self.vel_y = 0
        self.jump = False
        self.in_air = True


class World:

    def __init__(self, data):

        self.space_list = []

        dirt = pygame.image.load('C:/Users/juane/Images/GameImages/dirt.jpg')
        grass_and_dirt = pygame.image.load("C:/Users/juane/Images/GameImages/grass_and_dirt.jpg")

        row_counter = 0
        for row in data:
            column_counter = 0
            for space in row:
                if space == 1:
                    img = pygame.transform.scale(dirt, (SPACE_SIZE, SPACE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = column_counter * SPACE_SIZE
                    img_rect.y = row_counter * SPACE_SIZE
                    space = (img, img_rect)
                    self.space_list.append(space)
                if space == 2:
                    img = pygame.transform.scale(grass_and_dirt, (SPACE_SIZE, SPACE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = column_counter * SPACE_SIZE
                    img_rect.y = row_counter * SPACE_SIZE
                    space = (img, img_rect)
                    self.space_list.append(space)
                if space == 3:
                    enemy = Enemy(column_counter * SPACE_SIZE, row_counter * SPACE_SIZE)
                    enemy_group.add(enemy)
                if space == 4:
                    lava = Lava(column_counter * SPACE_SIZE, row_counter * SPACE_SIZE + (SPACE_SIZE - 35))
                    lava_group.add(lava)
                if space == 5:
                    door = Door(column_counter * SPACE_SIZE, row_counter * SPACE_SIZE - 25)
                    door_group.add(door)

                column_counter += 1
            row_counter += 1

    def draw(self):
        for space in self.space_list:
            screen.blit(space[0], space[1])
            # pygame.draw.rect(screen, (255, 255, 255), space[1], 1)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:/Users/juane/Images/GameImages/enemy.jpg')
        self.image = pygame.transform.scale(img, (SPACE_SIZE, SPACE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:/Users/juane/Images/GameImages/lava.jpg')
        self.image = pygame.transform.scale(img, (SPACE_SIZE, SPACE_SIZE - 15))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


class Door(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('C:/Users/juane/Images/GameImages/door.png')
        self.image = pygame.transform.scale(img, (SPACE_SIZE, int(SPACE_SIZE * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0


world_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0],
    [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [4, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 4, 4, 4, 2, 2, 2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]


player = Player(0, SCREEN_HEIGHT - 2 * SPACE_SIZE)
enemy_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
door_group = pygame.sprite.Group()
world = World(world_data)
restart_button = Button(SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 50, game_over_image)
start_button = Button(SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 25, start_image)
win_image = Win(SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 50, win_image)

running = True
while running:

    clock.tick(fps)
    screen.blit(sky_img, (0, 0))

    if main_menu:
        if start_button.draw():
            main_menu = False

    else:
        world.draw()

        if game_over == 0:
            enemy_group.update()

        enemy_group.draw(screen)
        lava_group.draw(screen)
        door_group.draw(screen)
        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                player.reset(0, SCREEN_HEIGHT - 2 * SPACE_SIZE)
                game_over = 0

        if game_over == 1:
            win_image.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()


pygame.quit()
