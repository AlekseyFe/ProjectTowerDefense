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

group_button_pay_tower = pygame.sprite.Group()

group_interfeic = pygame.sprite.Group()

coins = 100

size = (1200, 800)
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color("black"))
running = True
pygame.init()

CELL_SIZE = 50

X_Y_BASE = []

FRAGES = 0

LEFT = 10
TOP = 10

heatpoints = 10

coordinates_base = None


class Board:
    def __init__(self, map_game, width, height):
        self.map_game = map_game
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.width = width
        self.height = height
        self.flag = 1

    def render(self):
        for i in range(len(self.map_game)):
            for j in range(len(self.map_game[i])):
                if self.map_game[i][j] == "s":
                    pygame.draw.rect(screen, pygame.Color("blue"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                if self.map_game[i][j] == "e":
                    global coordinates_base
                    coordinates_base = [j, i]
                    # pygame.draw.rect(screen, pygame.Color("yellow"), (
                    #     self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))
                    #
                    # X_Y_BASE = (
                    #     self.left + j * self.cell_size + self.cell_size, self.top + i * self.cell_size + self.cell_size)

                if self.map_game[i][j] == "r":
                    pygame.draw.rect(screen, pygame.Color("brown"), (
                        self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

                if self.map_game[i][j] == "t":
                    pygame.draw.rect(screen, pygame.Color("green"), (
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
                # print(self.map_game[cell_coords[1]], type(self.map_game[cell_coords[1]]))
                # self.map_game[cell_coords[1]][cell_coords[0]] = "t_zanyat"
                global coordinates_click_tower
                object_pay_interfeic.active_window = True
                coordinates_click_tower = cell_coords
                # MachineGun(cell_coords[0], cell_coords[1])

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        print(cell)
        self.on_click(cell)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x_y_spawn, speed, enemy_tsel, damage):  # скорость пули в пикселях в секнуду
        super().__init__(all_sprites, group_bullet)
        self.speed = speed

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
        self.rect.x = self.x_bullet - 3 + self.x_change
        self.rect.y = self.y_bullet - 3 + self.y_change
        # self.rect.move(self.x_change,
        #                            нужно проверить как работает
        # self.y_change)

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

        self.draw_circle = True
        pygame.draw.circle(self.image, pygame.Color(200, 200, 200, 50),
                           (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)

        self.rect = pygame.Rect(senter_radiusa[0] - self.radius_of_the_fire,
                                senter_radiusa[1] - self.radius_of_the_fire,
                                self.radius_of_the_fire * 2,
                                self.radius_of_the_fire * 2)

    def drawing(self):
        if self.draw_circle == True:
            pygame.draw.circle(self.image, pygame.Color(200, 200, 200, 50),
                               (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)
        else:
            pygame.draw.circle(self.image, pygame.Color(200, 200, 200, 0),
                               (self.radius_of_the_fire, self.radius_of_the_fire), self.radius_of_the_fire)


class MachineGun(Tower):

    def __init__(self, x_cell, y_cell, rate_of_fire=5, radius_of_the_fire=150,
                 speed_of_the_bullet=5):
        super().__init__(x_cell, y_cell)  # нужно окрасить холст
        self.radius_of_the_fire = radius_of_the_fire
        self.rate_of_fire = rate_of_fire
        global coins
        self.time_next_shot = 1 / rate_of_fire
        self.speed_of_the_bullet = speed_of_the_bullet

        self.damage = 1

        coins -= 50

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

    def __init__(self, pos):

        super().__init__(all_sprites, group_enemy)

        if pos == 0:
            self.x_cell, self.y_cell = 2, 0

            self.vector = [[1, 0], [0, 1], [1, 0], [0, -1]]

        if pos == 1:
            self.x_cell, self.y_cell = 2, 11

            self.vector = [[0, -1], [1, 0], [0, -1]]

        if pos == 2:
            self.x_cell, self.y_cell = 13, 7

            self.vector = [[-1, 0], [0, -1], [1, 0], [0, -1]]

        self.x = LEFT + self.x_cell * CELL_SIZE

        self.y = TOP + self.y_cell * CELL_SIZE

        self.senter_enemy = [self.x + CELL_SIZE * 0.5, self.y + CELL_SIZE * 0.5]

        self.poten_heatpoints = 100

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA, 32)

        self.rect = pygame.Rect(self.x, self.y, CELL_SIZE, CELL_SIZE)

        pygame.draw.circle(self.image, pygame.Color("grey"), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2)

        self.speed = 0.2 / fps

        self.x_change = 0

        self.y_change = 0

        self.heatpoints = 100

        self.negative = False

        self.last_vector_x, self.last_vector_y = 0, 0

    def damage(self, damage):

        self.heatpoints -= damage

    def damage_poten(self, damage):

        self.poten_heatpoints -= damage

    def killer(self):
        global coins
        coins += 10
        self.kill()
        global FRAGES
        FRAGES += 1

    def update(self):

        if self.vector:

            # print(self.rect)

            self.x_change += self.vector[0][0] * self.speed

            self.y_change += self.vector[0][1] * self.speed

            self.check_in_board()

            if self.negative:

                self.rect = self.rect.move(-1 * self.last_vector_x * int(self.x_change),
                                           -1 * self.last_vector_y * int(self.y_change))

                self.senter_enemy[0] += -1 * self.last_vector_x * int(self.x_change)
                self.senter_enemy[1] += -1 * self.last_vector_y * int(self.y_change)

                self.x_change, self.y_change = 0, 0



            else:

                self.rect = self.rect.move(int(self.x_change), int(self.y_change))

                self.senter_enemy[0] += int(self.x_change)
                self.senter_enemy[1] += int(self.y_change)

        if self.heatpoints <= 0:
            self.killer()

    def check_in_board(self):

        if self.vector[0][0] == -1 or self.vector[0][1] == -1:

            j, i = (self.rect[0] - LEFT) // CELL_SIZE, (self.rect[1] - TOP) // CELL_SIZE



        else:

            j, i = (self.rect[0] + CELL_SIZE - LEFT - 1) // CELL_SIZE, (self.rect[1] + CELL_SIZE - 1 - TOP) // CELL_SIZE

        # print(i, j)

        # print(map_tower_defense[i][j])

        if map_tower_defense[i][j] == "e":

            self.vector.clear()



        elif map_tower_defense[i][j] != 'r':

            # print(self.rect)

            if self.vector[0][0] == -1 or self.vector[0][1] == -1:

                # print((self.rect[1] - TOP) % CELL_SIZE, (self.rect[0] - LEFT) % CELL_SIZE)

                self.x_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE

                self.y_change = (CELL_SIZE - (self.rect[0] - LEFT) % CELL_SIZE) % CELL_SIZE



            else:

                self.x_change = (self.rect[0] + CELL_SIZE - LEFT) % CELL_SIZE

                self.y_change = (self.rect[1] + CELL_SIZE - TOP) % CELL_SIZE

            self.last_vector_x, self.last_vector_y = self.vector[0]

            self.negative = True

            # print(self.x_change, self.y_change)

            del self.vector[0]

            # print("DELETE", self.vector)



        else:

            self.negative = False


class AllEnemys:

    def __init__(self):

        self.time_last_first_enemy = perf_counter()

        self.time_last_second_enemy = perf_counter()

        self.time_last_third_enemy = perf_counter()

        self.time_to_next_first = 4.0

        self.time_to_next_second = 4.0

        self.time_to_next_third = 4.0

        self.time_now_first = 0

        self.time_now_second = 0

        self.time_now_third = 0

    def new_enemy_first(self):

        self.time_now_first = perf_counter()

        if (self.time_now_first - self.time_last_first_enemy) >= self.time_to_next_first:
            self.time_last_first_enemy = perf_counter()

            return Enemy(0)

        # if FRAGES > 20:

        #     self.time_next_enemy = 2

    def new_enemy_second(self):

        self.time_now_second = perf_counter()

        if FRAGES > 40 and (self.time_now_second - self.time_last_second_enemy) >= self.time_to_next_second:
            self.time_last_second_enemy = perf_counter()

            return Enemy(1)

        # if FRAGES > 60:

        #     self.time_to_next_second = 2

    def new_enemy_third(self):

        self.time_now_third = perf_counter()

        if FRAGES > 80 and (self.time_now_third - self.time_last_third_enemy) >= self.time_to_next_third:
            self.time_last_third_enemy = perf_counter()

            return Enemy(2)

        # if FRAGES > 100:

        #     self.time_to_next_third = 2


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


class Base(pygame.sprite.Sprite):
    def __init__(self, x_cell, y_cell):
        super().__init__(all_sprites)

        self.x_cell = x_cell
        self.y_cell = y_cell

        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE),
                                    pygame.SRCALPHA, 32)
        x = LEFT + self.x_cell * CELL_SIZE
        y = TOP + self.y_cell * CELL_SIZE
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

        pygame.draw.rect(self.image, pygame.Color("violet"), (0, 0, CELL_SIZE, CELL_SIZE))

    def check_na_visit_enemy(self):
        spisok_vragov_na_base = pygame.sprite.spritecollide(self,
                                                            group_enemy,
                                                            False)
        if spisok_vragov_na_base != []:
            global heatpoints, coins
            for enemy in spisok_vragov_na_base:
                enemy.killer()
                heatpoints -= 1
                coins -= 10


class Pole_Interfeic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(group_interfeic)

        self.image = pygame.Surface((400, 800), pygame.SRCALPHA, 32)

        self.rect = pygame.Rect(800, 10, 400, 800)

        self.font = pygame.font.Font(None, 50)

        self.infa_coins_x = 200
        self.infa_coins_y = 50

        self.infa_heat_x = 25
        self.infa_heat_y = 50

        self.active_window = True

    def update(self, coins):
        self.image.fill(pygame.Color('black'))
        self.text_coins = self.font.render(f"Coins: {coins}", 1, (100, 255, 100))
        self.image.blit(self.text_coins, (self.infa_coins_x, self.infa_coins_y))
        self.text_heat = self.font.render(f"Heats: {heatpoints}", 1, (100, 255, 100))
        self.image.blit(self.text_heat, (self.infa_heat_x, self.infa_heat_y))


# class Main_spisok_tower(pygame.sprite.Sprite):
#     def __init__(self, ):
#
#

class Button_Yes(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(group_button_pay_tower)

        self.x = x
        self.y = y
        self.size_width_but = 70
        self.size_height_but = 50
        self.image = pygame.Surface((self.size_width_but, self.size_height_but), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, 100, 100)

        self.font = pygame.font.Font(None, 50)

    def drawing(self):
        self.image.fill(pygame.Color('black'))
        self.text = self.font.render("Да", 1, (100, 255, 100))
        text_x = 1
        text_y = 1

        text_w = self.text.get_width()
        text_h = self.text.get_height()

        pygame.draw.rect(self.image, (0, 255, 0), (0, 0,
                                                   self.size_width_but, self.size_height_but), 1)
        self.image.blit(self.text, (10, 10))

    def zalivka(self):
        self.image.fill(pygame.Color('black'))


class Button_No(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(group_button_pay_tower)

        self.x = x
        self.y = y
        self.size_width_but = 80
        self.size_height_but = 50
        self.image = pygame.Surface((self.size_width_but, self.size_height_but), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(x, y, 100, 100)

        self.font = pygame.font.Font(None, 50)

    def drawing(self):
        self.image.fill(pygame.Color('black'))
        self.text = self.font.render("Нет", 1, (100, 255, 100))
        text_x = 1
        text_y = 1

        text_w = self.text.get_width()
        text_h = self.text.get_height()

        pygame.draw.rect(self.image, (0, 255, 0), (0, 0,
                                                   self.size_width_but, self.size_height_but), 1)
        self.image.blit(self.text, (10, 10))

    def zalivka(self):
        self.image.fill(pygame.Color('black'))


class Pay_tower_interfeic(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(group_interfeic)

        self.image = pygame.Surface((300, 500), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(850, 300, 400, 400)

        self.font = pygame.font.Font(None, 50)

        self.active_window = False

        self.object_button_yes = Button_Yes(875, 375)
        self.object_button_no = Button_No(1025, 375)

    def update(self, coins):
        if self.active_window:
            self.image.fill(pygame.Color('black'))
            self.text = self.font.render("Купить башню?", 2, (100, 255, 100))

            text_x = 1
            text_y = 1

            text_w = self.text.get_width()
            text_h = self.text.get_height()
            self.object_button_yes.drawing()
            self.object_button_no.drawing()
            pygame.draw.rect(self.image, (0, 255, 0), (0, 0,
                                                       text_w + 20, text_h + 100), 1)
            self.image.blit(self.text, (10, 10))



        else:
            self.image.fill(pygame.Color('black'))
            self.object_button_yes.zalivka()
            self.object_button_no.zalivka()


Pole_Interfeic()

object_pay_interfeic = Pay_tower_interfeic()

running = True
with open('map_tower_defense_1.txt', 'r', encoding='utf8') as f:
    map_tower_defense = f.readlines()
    for k in range(len(map_tower_defense)):
        map_tower_defense[k] = map_tower_defense[k].split()
print(map_tower_defense)

board = Board(map_tower_defense, len(map_tower_defense[0]), len(map_tower_defense))
board.render()

object_Base = Base(coordinates_base[0], coordinates_base[1])

coordinates_click_tower = None
circle_of_tower = None

enemys = AllEnemys()

pause = False

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                board.get_click(event.pos)
                if object_pay_interfeic.active_window == True and coordinates_click_tower != None:
                    if (object_pay_interfeic.object_button_yes.x < event.pos[
                        0] < object_pay_interfeic.object_button_yes.x + object_pay_interfeic.object_button_yes.size_width_but) and (
                            object_pay_interfeic.object_button_yes.y < event.pos[
                        1] < object_pay_interfeic.object_button_yes.y + object_pay_interfeic.object_button_yes.size_height_but):
                        board.map_game[coordinates_click_tower[1]][coordinates_click_tower[0]] = "t_zanyat"
                        a = MachineGun(coordinates_click_tower[0], coordinates_click_tower[1])
                        circle_of_tower = a.object_RadiusFire
                        for tower in group_tower:
                            tower.object_RadiusFire.draw_circle = False
                        circle_of_tower.draw_circle = True

                        # if circle_of_tower != None:
                        #     circle_of_tower.draw_circle = False
                        object_pay_interfeic.active_window = False

                if object_pay_interfeic.active_window == True and coordinates_click_tower != None:
                    if (object_pay_interfeic.object_button_no.x < event.pos[
                        0] < object_pay_interfeic.object_button_no.x + object_pay_interfeic.object_button_no.size_width_but) and (
                            object_pay_interfeic.object_button_no.y < event.pos[
                        1] < object_pay_interfeic.object_button_no.y + object_pay_interfeic.object_button_no.size_height_but):
                        object_pay_interfeic.active_window = False

                for tower in group_tower:
                    # if tower.rect.collidepoint(event.pos) and circle_of_tower == None:
                    #     tower.object_RadiusFire.draw_circle = True
                    #     print(tower.object_RadiusFire.draw_circle)
                    #     circle_of_tower = tower.object_RadiusFire
                    if tower.rect.collidepoint(event.pos) and circle_of_tower != tower.object_RadiusFire:
                        print(1)
                        circle_of_tower.draw_circle = False
                        tower.object_RadiusFire.draw_circle = True
                        circle_of_tower = tower.object_RadiusFire
                    if tower.rect.collidepoint(event.pos) and circle_of_tower == tower.object_RadiusFire:
                        circle_of_tower.draw_circle = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                if pause == False:
                    pause = True
                else:
                    pause = False

    if pause == False:
        for tower in group_tower:
            tower.update()
            tower.object_RadiusFire.drawing()

        for bullet in group_bullet:
            bullet.update()
            bullet.check_collide_bullet_with_enemy()

        for enemy in group_enemy:
            enemy.update()

        object_Base.check_na_visit_enemy()

        enemys.new_enemy_first()

        enemys.new_enemy_second()

        enemys.new_enemy_third()

    for inter in group_interfeic:
        inter.update(coins)

    if perf_counter() > 7:
        FRAGES = 50

    if perf_counter() > 10:
        FRAGES = 70

    if perf_counter() > 15:
        FRAGES = 110

    # group_bullet.update(enemy)
    board.render()
    group_interfeic.draw(screen)
    group_button_pay_tower.draw(screen)
    all_sprites.draw(screen)
    clock.tick(60)
    pygame.display.flip()