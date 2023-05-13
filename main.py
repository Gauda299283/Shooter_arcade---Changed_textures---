import pygame as pg
import random

# Иниацилизация
pg.init()

# Класс для спрайтов
class MySprite(pg.sprite.Sprite):
    # Конструктор
    def __init__(self, image:str, pos:list, size:list, speed:float):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(pg.image.load(image), (size[0], size[1]))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.recharge = 0.75
        self.recharged = self.recharge * fps

    # Функция для отрисовки
    def re_draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс игрока
class Player(MySprite):
    # Функция для создания снаряда
    def fire(self):
        # Создание и добаление пули
        if self.recharged <= 0:
            bullets.add(GranadeButBullet('source/image/Granade.png', [self.rect.x + 10, self.rect.centery], [25, 25], 5))
            shoot_sound.play()
            self.recharged = self.recharge * fps

    # Функция для обновления 
    def update(self):
        # Получаем список последних нажатых кнопак
        keys = pg.key.get_pressed()

        # Движение игрока
        if keys[pg.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[pg.K_RIGHT] and self.rect.x < ww - 55:
            self.rect.x += self.speed

        if keys[pg.K_UP]:
            self.fire()

        self.recharged -= 1

# Класс детя
class Kid(MySprite):
    # Функция для обновления
    def update(self):
        global lost

        # Движенгие дитя вниз
        self.rect.y += self.speed

        # Проверка, вышел ли ребенок за окно
        if self.rect.y > wh:
            # Изменение позицииh
            self.rect.y = -50
            self.rect.x = random.randint(50, ww-50)
            # Добавлдение шкеда в "Потерянные"
            lost += 1

# Класс террориста
class Terrorist(MySprite):
    # Функция для обновления
    def update(self):
        global lost

        # Движенгие дитя вниз
        self.rect.y += self.speed

        # Проверка, вышел ли ребенок за окно
        if self.rect.y > wh:
            # Изменение позиции
            self.rect.y = -random.randint(0, 700)
            self.rect.x = random.randint(50, ww-50)
            # Добавлдение шкеда в "Потерянные"

# Клосс снаряда
class GranadeButBullet(MySprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

# Ширина и высота окна
ww, wh = 500, 700

# Системное
fps = 60
pg.mouse.set_visible(False)

# Создание часов
Clock = pg.time.Clock()

# Создание текстов
my_font = pg.font.Font(pg.font.get_default_font(), 32)

# Звуки
pg.mixer.music.load('source/sound/Music.ogg')
pg.mixer.music.set_volume(0.1)
pg.mixer.music.play()

shoot_sound = pg.mixer.Sound('source/sound/fire.ogg')

# Картинки
bg_image = pg.transform.scale(pg.image.load('source/image/bg.jpg'), (ww, wh))

# Создания окна
window = pg.display.set_mode((ww, wh)) 
pg.display.set_caption('Шутер')

# Игровой цикл
App = True
while App:
    # Пауза
    pause = False

    # Счетчики
    lost = 0
    score = 0

    # Создание игрока
    granade = Player('source/image/Granade.png', [225, 620], [50, 50], 2)

    # Список детей
    kids = pg.sprite.Group()

    # Список пуль
    bullets = pg.sprite.Group()

    # Список террористов
    terrorists = []

    # Создание Террориста
    for i in range(10):
        terrorists.append(Terrorist('source\image\Terror.png', [random.randint(50, ww-50), -random.randint(0, 700)], [70, 50], 2))

    # Добавление детей в список детей
    for i in range(10):
        kids.add(Kid('source/image/kids.png', [random.randint(50, ww-50), -random.randint(50, 500)], [100, 50], random.randint(1, 2)))

    # Второй игровой цикл
    Go = True
    while Go:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                App = False
                Go = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    pause = True if pause == False else False
        
        # Если не включена пауза
        if not pause:
            # Отрисовка заднего фона
            window.blit(bg_image, (0, 0))

            # Отрисовка и обработка пуль
            bullets.draw(window)
            bullets.update()

            # Отрисовка и обработка детей
            for terrorist in terrorists:
                terrorist.re_draw()
                terrorist.update()

            # Отрисовка и обработка детей
            kids.draw(window)
            kids.update()

            # Отрисовка и обработка гранаты
            granade.re_draw()
            granade.update()

            # Проверка на столкновение
            collides = pg.sprite.groupcollide(bullets, kids, True, True)

        # Если пауза
        else:
            text_pause = my_font.render('||', True, (255, 255, 255))
            text_pause_w = text_pause.get_width()
            text_pause_h = text_pause.get_height()
            window.blit(text_pause, ((ww - text_pause_w)//2, (wh - text_pause_h)//2))

        if pg.sprite.spritecollide(granade, kids, False) or lost >= 5:
            Go = False

            text_gameover = my_font.render('Ты ПРОИГРАЛ!', True, (255, 0, 0))
            text_gameover_w = text_gameover.get_width()
            text_gameover_h = text_gameover.get_height()
            window.blit(text_gameover, ((ww - text_gameover_w)//2, (wh - text_gameover_h)//2))

        if score >= 20:
            Go = False

            text_gameover = my_font.render('Ты ВЫЙГРАЛ!', True, (0, 255, 0))
            text_gameover_w = text_gameover.get_width()
            text_gameover_h = text_gameover.get_height()
            window.blit(text_gameover, ((ww - text_gameover_w)//2, (wh - text_gameover_h)//2))

        # Добавление очков и создание нового врага
        for i in range(len(collides)):
            score += 1
            kids.add(Kid('source/image/kids.png', [random.randint(50, ww-50), -random.randint(50, 500)], [100, 50], random.randint(1, 2)))

        # Вывод счетов
        text_lost = my_font.render(f'Пропущено: {lost}', True, (255, 255, 255))
        window.blit(text_lost, (10, 10))

        text_score = my_font.render(f'Счет: {score}', True, (255, 255, 255))
        window.blit(text_score, (10, 50))

        # Обновление окна
        pg.display.update()
        Clock.tick(fps)

pg.quit()