import pygame
from math import sqrt
from time import perf_counter

START = "s"
END = "e"
ROAD = "r"
PLACE_TOWER = "t"

clock = pygame.time.Clock()
fps = 10

all_sprites = pygame.sprite.Group()
group_bullet = pygame.sprite.Group()
group_enemy = pygame.sprite.Group()
group_tower = pygame.sprite.Group()

size = (800, 600)
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("black"))
running = True
pygame.init()

CELL_SIZE = 50

X_Y_BASE = []

LEFT = 10
TOP = 10


class Board:
    def __init__(self, map_game, width, height):
        self.map_game = map_game
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.width = width
        self.height = height

    def render(self):
        for i in range(len(self.map_game)):
            for j in range(len(self.map_game[i])):
                if self.map_game[i][j] == "s":
                    pygame.draw.rect(screen, pygame.Color("blue"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                if self.map_game[i][j] == "e":
                    pygame.draw.rect(screen, pygame.Color("yellow"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                    X_Y_BASE = (
                        self.left + j * self.cell_size + self.cell_size, self.top + i * self.cell_size + self.cell_size)

                if self.map_game[i][j] == "r":
                    pygame.draw.rect(screen, pygame.Color("brown"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        stroka_kletki = (x - self.left) // self.cell_size
        stolbes_kletki = (y - self.top) // self.cell_size
        print(self.width, self.height)
        if stroka_kletki > self.width - 1 or stolbes_kletki > self.height - 1 or stroka_kletki < 0 or stolbes_kletki < 0:
            return None
        else:
            return (stroka_kletki, stolbes_kletki)

    def on_click(self, cell_coords):
        if cell_coords != None:
            if self.map_game[cell_coords[1]][cell_coords[0]] == "t":
                print(self.map_game[cell_coords[1]], type(self.map_game[cell_coords[1]]))
                self.map_game[cell_coords[1]][cell_coords[0]] = "t_zanyat"
                MachineGun(cell_coords[0], cell_coords[1])

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        self.on_click(cell)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_y_spawn, speed, enemy_tsel, damage):  # скорость пули в пикселях в секнуду
        super().__init__(all_sprites, group_bullet)
        self.speed = 5

        self.damage = damage
        self.size_bullet = (6, 6)
        self.image = pygame.Surface(self.size_bullet, pygame.SRCALPHA, 32)

        self.rect = pygame.Rect(x_y_spawn[0] - self.size_bullet[0] * 0.5, x_y_spawn[1] - self.size_bullet[1] * 0.5,
                                self.size_bullet[0], self.size_bullet[1])
        pygame.draw.circle(self.image, pygame.Color("red"), (3, 3), 3)
        self.x_bullet = x_y_spawn[0]
        self.y_bullet = x_y_spawn[1]
        self.enemy_tsel = enemy_tsel


        self.x_change = 0  # накапливаем в этих переменных вещественные числа сдвига по х и по у
        self.y_change = 0
        self.t1_puli = perf_counter()



    def killer(self):
        self.kill()

    def check_collide_bullet_with_enemy(self):
        if pygame.sprite.collide_rect(self.enemy_tsel, self):
            self.enemy_tsel.damage(self.damage)
            self.kill()

    def update(self):

        self.put_do_enemy = sqrt((self.enemy_tsel.senter_enemy[0] - self.x_bullet) ** 2 + (
                self.enemy_tsel.senter_enemy[1] - self.y_bullet) ** 2)

        self.vector_x_bullet = (self.enemy_tsel.senter_enemy[
                                    0] - self.x_bullet) / self.put_do_enemy  # высчитываем на сколько
        # пуля должна сместится в условную единицу времени
        self.vector_y_bullet = (self.enemy_tsel.senter_enemy[1] - self.y_bullet) / self.put_do_enemy

        self.x_change = self.vector_x_bullet * self.speed
        self.y_change = self.vector_y_bullet * self.speed
        self.x_bullet = self.x_bullet + self.x_change
        self.y_bullet = self.y_bullet + self.y_change
        # print(self.rect.x, self.x_change, end = " ")
        self.rect.x =  self.x_bullet - 3 + self.x_change
        self.rect.y =  self.y_bullet - 3 + self.y_change
        # self.rect.move(self.x_change,
        #                            нужно проверить как работает
                                   # self.y_change)
        print(self.rect, self.x_bullet, self.y_bullet)

        self.check_collide_bullet_with_enemy()


class Tower(pygame.sprite.Sprite):
    def __init__(self, x_cell, y_cell):
        super().__init__(all_sprites, group_tower)
        self.x_cell = x_cell
        self.y_cell = y_cell

        x = LEFT + self.x_cell * CELL_SIZE
        y = TOP + self.y_cell * CELL_SIZE
        self.x_y_left_top_angle_cell_tower = (x, y)
        self.senter_cell_tower = (x + 0.5 * CELL_SIZE, y + 0.5 * CELL_SIZE)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def killer(self):  # удаляем башню, если не нужна
        self.kill()




class RadiusFire(pygame.sprite.Sprite):
    def __init__(self, senter_radiusa, radius_of_the_fire):
        super().__init__(all_sprites)
        self.radius_of_the_fire = radius_of_the_fire
        self.image = pygame.Surface((2 * self.radius_of_the_fire, 2 * self.radius_of_the_fire),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color(200, 200, 200, 50),
                           (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)

        self.rect = pygame.Rect(senter_radiusa[0] - self.radius_of_the_fire, senter_radiusa[1] - self.radius_of_the_fire,
                                self.radius_of_the_fire * 2,
                                self.radius_of_the_fire * 2)


class MachineGun(Tower):
    def __init__(self, x_cell, y_cell, rate_of_fire=10, radius_of_the_fire=150,
                 speed_of_the_bullet=1):
        super().__init__(x_cell, y_cell)  # нужно окрасить холст
        self.radius_of_the_fire = radius_of_the_fire
        self.rate_of_fire = rate_of_fire

        self.time_next_shot = 1 / rate_of_fire
        self.speed_of_the_bullet = speed_of_the_bullet

        self.damage = 5

        pygame.draw.rect(self.image, pygame.Color("orange"), (0, 0, CELL_SIZE, CELL_SIZE))

        self.object_RadiusFire = RadiusFire(self.senter_cell_tower, self.radius_of_the_fire)
        self.time_last_shot = perf_counter()

    # def shot(self):
    #     self.spisok_vragov_na_change = pygame.sprite.spritecollide(self.object_RadiusFire.image_radius_of_fire,
    #                                                                group_enemy)  # надо найти ближайшего к базе врага
    #     self.2puti_do_base = list(map(
    #         lambda s: sqrt((s.x_enemy - self.senter_cell_tower[0]) ** 2 + (s.y_enemy - self.senter_cell_tower[1]) ** 2),
    #         self.spisok_vragov_na_change))
    #     self.enemy_tsel = self.spisok_vragov_na_change.index(min(self.puti_do_base))
    #
    #     Bullet(self.senter_cell_tower, self.speed_of_the_bullet, self.enemy_tsel, self.damage)

    def update(self):
        self.time_current = perf_counter()
        if self.time_current - self.time_last_shot >= self.time_next_shot:

            # print(perf_counter())
            spisok_vragov_na_change = pygame.sprite.spritecollide(self.object_RadiusFire,
                                                                  group_enemy,
                                                                  False)  # надо найти ближайшего к базе врага
            if len(spisok_vragov_na_change) != 0:
                puti_do_base = list(map(
                    lambda s: sqrt(
                        (s.senter_enemy[0] - self.senter_cell_tower[0]) ** 2 + (
                                s.senter_enemy[1] - self.senter_cell_tower[1]) ** 2),
                    spisok_vragov_na_change))
                enemy_tsel = spisok_vragov_na_change[puti_do_base.index(min(puti_do_base))]
                if enemy_tsel.poten_heatpoints > 0:

                    Bullet(self.senter_cell_tower, self.speed_of_the_bullet, enemy_tsel, self.damage)
                    enemy_tsel.damage_poten(self.damage)
                    self.time_last_shot = perf_counter()


class Artillery(Tower):
    def __init__(self, x_kletki_razmechenia, y_kletki_razmechenia, rate_of_fire, radius_of_the_fire=50,
                 speed_of_the_bullet=5, type_of_amunition="base"):
        super.__init__(x_kletki_razmechenia, y_kletki_razmechenia)  # нужно окрасить холст
        self.radius_of_the_fire = radius_of_the_fire
        self.rate_of_fire = rate_of_fire
        self.speed_of_the_bullet = speed_of_the_bullet

        self.damage = 50

        pygame.draw.rect(self.image_tower, pygame.Color("pink"), (0, 0, CELL_SIZE, CELL_SIZE))

        class RadiusFire(pygame.sprite.Sprite):
            def __init__(self):
                super.__init__(all_sprites)
                self.image_radius_of_fire = pygame.Surface((2 * self.radius_of_the_fire, 2 * self.radius_of_the_fire),
                                                           pygame.SRCALPHA, 32)

            pygame.draw.circle(self.image_radius_of_fire, pygame.Color("purple"),
                               (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)

        class RadiusFragments(pygame.sprite.Sprite):
            def __init__(self):
                super.__init__(all_sprites)
                self.image_radius_fragments = pygame.Surface((2 * self.radius_fragments, 2 * self.radius_fragments),
                                                             pygame.SRCALPHA, 32)
                self.image_radius_fragments.rect = self.image_radius_fragments.get_rect()
                # pygame.draw.circle(self.image_radius_fragments, pygame.Color("purple"),
                #                    (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)

        self.object_RadiusFire = RadiusFire()
        self.object_RadiusFragments = RadiusFragments()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_cell, y_cell):
        super().__init__(all_sprites, group_enemy)
        self.x_cell = x_cell
        self.y_cell = y_cell


        self.poten_heatpoints = 10000

        self.x = LEFT + x_cell * CELL_SIZE
        self.y = TOP + y_cell * CELL_SIZE
        self.senter_enemy = (self.x + CELL_SIZE * 0.5, self.y + CELL_SIZE * 0.5)

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)
        pygame.draw.circle(self.image, pygame.Color("grey"), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)

        self.heatpoints = 10000

    def damage(self, damage):
        self.heatpoints -= damage

    def damage_poten(self, damage):
        self.poten_heatpoints -= damage

    def killer(self):
        self.kill()

    def update(self):
        self.rect.x += 1
        self.senter_enemy =  list(self.senter_enemy)
        self.senter_enemy[0] += 1
        if self.heatpoints <= 0:
            self.killer()


class BulletArtillery(Bullet):
    def __init__(self, x_y_spawn, speed_of_the_bullet, enemy_tsel, damage, radius_fragments):
        super.__init__(x_y_spawn, speed_of_the_bullet, enemy_tsel, damage)
        self.radius_fragments = radius_fragments

    def check_collide_bullet_with_enemy(self):
        if pygame.sprite.sprite.collide_rect(self.enemy_tsel, self):
            vragi = pygame.sprite.spritecollide(self.radius_fragments, group_enemy)
            self.enemy_tsel.damage(self.damage)
            for enemy in vragi:
                self.enemy.damage(self.damage)
            self.kill()


running = True
with open('map_tower_defense_1.txt', 'r', encoding='utf8') as f:
    map_tower_defense = f.readlines()
    for k in range(len(map_tower_defense)):
        map_tower_defense[k] = map_tower_defense[k].split()
print(map_tower_defense)

board = Board(map_tower_defense, len(map_tower_defense[0]), len(map_tower_defense))
board.render()

MachineGun(3, 2)
MachineGun(8, 2)
Enemy(2, 1)
Enemy(0, 1)

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                board.get_click(event.pos)

    for tower in group_tower:
        tower.update()

    for bullet in group_bullet:
        bullet.update()
        bullet.check_collide_bullet_with_enemy()

    for enemy in group_enemy:
        enemy.update()
        pygame.draw.rect()

    #group_bullet.update(enemy)
    board.render()
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()
