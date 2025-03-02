import pygame
import random

# Импорт необходимых модулей, включая Pygame и собственные классы
from objects import Player, Bar, Ball, Block, ScoreCard, Message, Particle, generate_particles

# Инициализация Pygame
pygame.init()
# Определение размеров экрана
SCREEN = WIDTH, HEIGHT = 288, 512

# Получение информации о текущем разрешении дисплея
info = pygame.display.Info()
width = info.current_w
height = info.current_h

# Установка режима отображения в зависимости от соотношения сторон
if width >= height:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
    win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

# Настройка часов для управления частотой кадров
clock = pygame.time.Clock()
FPS = 45

# Определение цветов в формате RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (54, 69, 79)
c_list = [RED, BLACK, WHITE]  # Список используемых цветов

# Инициализация шрифтов
pygame.font.init()
score_font = pygame.font.Font('Fonts/BubblegumSans-Regular.ttf', 50)

# Загрузка звуковых эффектов
coin_fx = pygame.mixer.Sound('Sounds/coin.mp3')   # Звук получения монеты
death_fx = pygame.mixer.Sound('Sounds/death.mp3')  # Звук смерти
move_fx = pygame.mixer.Sound('Sounds/move.mp3')    # Звук движения

# Загрузка изображений фонов и их масштабирование
bg_list = []
for i in range(1, 5):
    if i == 2:
        ext = "jpeg"  # Для второго изображения используем формат jpeg
    else:
        ext = "jpg"   # Остальные в формате jpg
    img = pygame.image.load(f"Assets/Backgrounds/bg{i}.{ext}")  # Загрузка изображения фона
    img = pygame.transform.scale(img, (WIDTH, HEIGHT))         # Масштабирование до размера экрана
    bg_list.append(img)                                          # Добавление изображения в список

# Загрузка фона на домашней странице
home_bg = pygame.image.load(f"Assets/Backgrounds/home.jpeg") 
bg = home_bg  # Установка фона игры

# Создание групп спрайтов для управления различными объектами
bar_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
block_group = pygame.sprite.Group()
destruct_group = pygame.sprite.Group()
win_particle_group = pygame.sprite.Group()

# Задаем параметры
bar_gap = 120
particles = []

# Создаем игрока и счётчик очков
p = Player(win)  
score_card = ScoreCard(140, 40, win)

# Функция для создания частиц при уничтожении игрока
def destroy_bird():
    x, y = p.rect.center  # Получаем координаты игрока
    for i in range(50):
        c = random.choice(c_list)  # Выбираем случайный цвет для каждой частицы
        particle = Particle(x, y, 1, c, win)  # Создаем частицу
        destruct_group.add(particle)  # Добавляем её в группу

# Функция для создания частиц при победе
def win_particles():
    for x, y in [(40, 120), (WIDTH - 20, 240), (15, HEIGHT - 30)]:
        for i in range(10):
            particle = Particle(x, y, 2, WHITE, win)  # Создание белых частиц для победы
            win_particle_group.add(particle)          # Добавление их в группу

# Сообщения об игре с использованием пользовательских шрифтов
title_font = "Fonts/Robus-BWqOd.otf"
dodgy = Message(134, 90, 100, "Angry", title_font, WHITE, win)
walls = Message(164, 145, 80, "Walls", title_font, WHITE, win)

tap_to_play_font = "Fonts/DebugFreeTrial-MVdYB.otf"
tap_to_play = Message(144, 400, 32, "TAP TO PLAY", tap_to_play_font, WHITE, win)
tap_to_replay = Message(144, 400, 30, "Tap to Replay", tap_to_play_font, WHITE, win)

# Переменные для отслеживания состояния игры
bar_width_list = [i for i in range(40, 150, 10)]  # Список возможных ширин баров
bar_frequency = 1200  # Частота появления баров
bar_speed = 4  # Скорость движения баров
touched = False  # Флаг касания
pos = None  # Позиция касания
home_page = True  # Флаг для домашней страницы
score_page = False  # Флаг для страницы счёта
bird_dead = False  # Флаг для состояния игрока
score = 0  # Текущий счёт
high_score = 0  # Рекордный счёт
move_left = False  # Флаг для движения влево
move_right = True  # Флаг для движения вправо
prev_x = 0  # Предыдущая позиция по X
p_count = 0  # Счётчик для частиц

# Главный игровой цикл
running = True
while running:
    win.blit(bg, (0, 0))  # Отображение фона

    # Обработка событий в игре
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Закрытие игры при выходе

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False  # Закрытие игры при нажатии клавиши Escape

        # Обработка касаний мыши на главной странице или странице счёта
        if event.type == pygame.MOUSEBUTTONDOWN and (home_page or score_page):
            home_page = False
            score_page = False
            win_particle_group.empty()  # Очистка ранее создавшихся частиц
            
            bg = random.choice(bg_list)  # Случайный выбор фона
            
            particles = []  # Сброс частиц
            last_bar = pygame.time.get_ticks() - bar_frequency
            next_bar = 0
            bar_speed = 4
            bar_frequency = 1200
            bird_dead = False  # Сброс состояния игрока
            score = 0  # Сброс счёта
            p_count = 0  # Сброс счётчика
            score_list = []  # Список очков
            
            # Создание блоков в случайных позициях
            for _ in range(15):
                x = random.randint(30, WIDTH - 30)
                y = random.randint(60, HEIGHT - 60)
                max = random.randint(8, 16)
                b = Block(x, y, max, win)  # Создание блока
                block_group.add(b)  # Добавляем блок в группу

        # Обработка касания мыши по игроку
        if event.type == pygame.MOUSEBUTTONDOWN and not home_page:
            if p.rect.collidepoint(event.pos):
                touched = True  # Игрок коснулся экрана
                x, y = event.pos
                offset_x = p.rect.x - x  # Вычисляем смещение по X

        if event.type == pygame.MOUSEBUTTONUP and not home_page:
            touched = False  # Завершение касания

        # Обработка движения мыши
        if event.type == pygame.MOUSEMOTION and not home_page:
            if touched:
                x, y = event.pos
                if move_right and prev_x > x:
                    move_right = False  # Меняем направление на влево
                    move_left = True
                    move_fx.play()  # Играем звук движения
                if move_left and prev_x < x:
                    move_right = True  # Меняем направление на вправо
                    move_left = False
                    move_fx.play()  # Играем звук движения

                prev_x = x  # Обновляем предыдущую позицию по X
                p.rect.x = x + offset_x  # Перемещение игрока

    # Если мы на домашней странице
    if home_page:
        bg = home_bg  # Используем домашний фон
        particles = generate_particles(p, particles, WHITE, win)  # Генерация частиц
        dodgy.update()  # Обновляем сообщения
        walls.update()  
        tap_to_play.update()
        p.update()  # Обновляем игрока
        
    # Если мы на странице счёта
    elif score_page:
        bg = home_bg  # Используем домашний фон
        particles = generate_particles(p, particles, WHITE, win)  
        tap_to_replay.update()  # Обновляем сообщение о повторной игре
        p.update()  # Обновляем игрока
        score_msg.update()  # Обновляем сообщение со счётом
        score_point.update()  # Обновляем очки
        if p_count % 5 == 0:  # Генерация частиц при каждых 5 очках
            win_particles()
        p_count += 1
        win_particle_group.update()  # Обновление группы частиц
        
    else:
        # Управление баром и шаром во время игры
        next_bar = pygame.time.get_ticks()  # Получаем текущее время в миллисекундах
        if next_bar - last_bar >= bar_frequency and not bird_dead:
            bwidth = random.choice(bar_width_list)  # Случайный выбор ширины бара
            
            # Создание верхней и нижней части баров
            b1prime = Bar(0, 0, bwidth + 3, GRAY, win) 
            b1 = Bar(0, -3, bwidth, WHITE, win)
            b2prime = Bar(bwidth + bar_gap + 3, 0, WIDTH - bwidth - bar_gap, GRAY, win)
            b2 = Bar(bwidth + bar_gap, -3, WIDTH - bwidth - bar_gap, WHITE, win)
            
            # Добавляем бары в группу
            bar_group.add(b1prime)
            bar_group.add(b1)
            bar_group.add(b2prime)
            bar_group.add(b2)

            color = random.choice(["red", "white"])  # Случайный выбор цвета шара
            pos = random.choice([0, 1])  # Случайный выбор позиции для шара
            if pos == 0:
                x = bwidth + 12
            elif pos == 1:
                x = bwidth + bar_gap - 12
            
            # Создание шара и добавление его в группу
            ball = Ball(x, 10, 1, color, win)
            ball_group.add(ball)
            last_bar = next_bar  # Обновляем последнее время создания бара
            
        # Проверка коллизий между шаром и игроком
        for ball in ball_group:
            if ball.rect.colliderect(p):  # Если шар касается игрока
                if ball.color == "white":
                    ball.kill()  # Уничтожаем белый шар
                    coin_fx.play()  # Звук получения монеты
                    score += 1  # Увеличиваем счёт
                    if score > high_score:
                        high_score += 1  # Обновляем рекордный счёт
                    score_card.animate = True  # Запустим анимацию счётчика
                elif ball.color == "red":
                    if not bird_dead:  # Если игрок не мёртв
                        death_fx.play()  # Проигрываем звук смерти
                        destroy_bird()  # Создаём частицы разрушения
                    bird_dead = True  # Игрок мёртв
                    bar_speed = 0  # Остановка баров
    
        # Проверка коллизий между игроком и барами
        if pygame.sprite.spritecollide(p, bar_group, False):
            if not bird_dead:
                death_fx.play()  # Проигрываем звук смерти
                destroy_bird()  # Создаём частицы разрушения
            bird_dead = True  # Игрок мёртв
            bar_speed = 0  # Остановка баров
        
        block_group.update()  # Обновляем блоки
        bar_group.update(bar_speed)  # Обновляем бары
        ball_group.update(bar_speed)  # Обновляем шары
        
        if bird_dead:
            destruct_group.update()  # Обновляем группу разрушающихся частиц
        
        score_card.update(score)  # Обновляем счёт
        
        if not bird_dead:
            particles = generate_particles(p, particles, WHITE, win)  # Генерация частиц для игрока
            p.update()  # Обновляем игрока

        # Увеличение сложности по мере накопления очков
        if score and score % 10 == 0:
            rem = score // 10
            if rem not in score_list:
                score_list.append(rem)  # Добавляем результат в список
                bar_speed += 1  # Увеличиваем скорость баров
                bar_frequency -= 200  # Уменьшаем частоту появления баров
                
        # Если игрок мёртв и нет частиц разрушения
        if bird_dead and len(destruct_group) == 0:
            score_page = True  # Переход на страницу счёта
            font = "Fonts/BubblegumSans-Regular.ttf"
            if score < high_score:  # Сообщение о текущем счёте
                score_msg = Message(144, 60, 55, "Score", font, WHITE, win)
            else:  # Сообщение о новом рекорде
                score_msg = Message(144, 60, 55, "New High", font, WHITE, win)
            
            score_point = Message(144, 110, 45, f"{score}", font, WHITE, win)  # Отображение очков
        
        # Если мы на странице счёта
        if score_page:
            block_group.empty()  # Очищаем блоки
            bar_group.empty()  # Очищаем бары
            ball_group.empty()  # Очищаем шары
            
            p.reset()  # Сброс игрока

    # Ограничиваем частоту кадров
    clock.tick(FPS)
    pygame.display.update()  # Обновление экрана

pygame.quit()  # Завершение работы Pygame