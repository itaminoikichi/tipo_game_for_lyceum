import pygame
import random

# Определение размеров экрана
SCREEN = WIDTH, HEIGHT = 288, 512

# Инициализация модуля шрифтов Pygame
pygame.font.init()


class Player:
    def __init__(self, win):
        self.win = win  # Хранение ссылки на объект окна
        
        # Загрузка изображения игрока и его масштабирование
        self.image = pygame.image.load(f"Assets/sf.png")
        self.image = pygame.transform.scale(self.image, (44, 44))
        self.reset()  # Инициализация начального положения игрока
        
    def update(self):
        # Отображение игрока на экране
        self.win.blit(self.image, self.rect)
        
    def reset(self):
        # Установка начальных координат игрока и получение прямоугольника изображения
        self.x = 145
        self.y = 270
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, width, color, win):
        # Инициализация спрайта баров
        super(Bar, self).__init__()
        
        # Создание прямоугольника бара
        self.rect = pygame.Rect(x, y, width, 20, border_radius=8)
        self.win = win  # Хранение ссылки на объект окна
        self.color = color  # Цвет бара
        
    def update(self, speed):
        # Движение бара вниз по экрану
        self.rect.y += speed
        if self.rect.y >= HEIGHT:  # Удаление бара, если он вышел за пределы экрана
            self.kill()
        self.win.fill(self.color, self.rect)  # Отображение бара


class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, type, color, win):
        # Инициализация спрайта шара
        super(Ball, self).__init__()
        
        self.x = x  # Начальная позиция по X
        self.y = y  # Начальная позиция по Y
        self.color = color  # Цвет шара
        self.win = win  # Хранение ссылки на объект окна

        # Определение цвета шара из словаря
        color_dict = {"red": (255, 0, 0), "white": (255, 255, 255), "gray": (54, 69, 79)}
        self.c = color_dict[self.color]  # Цвет шара
        self.rect = pygame.draw.circle(win, self.c, (x, y), 5)  # Рисуем шар с радиусом 5 на начальной позиции
        
        self.gray = color_dict["gray"]  # Серый цвет для отрисовки тени
        
    def update(self, speed):
        # Движение шара вниз
        self.y += speed
        if self.y >= HEIGHT:  # Удаление шара, если он вышел за пределы экрана
            self.kill()
        
        # Отрисовка тени шара и самого шара
        pygame.draw.circle(self.win, self.gray, (self.x + 2, self.y + 2), 6)
        self.rect = pygame.draw.circle(self.win, self.c, (self.x, self.y), 6)


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, max, win):
        # Инициализация спрайта блока
        super(Block, self).__init__()
        
        self.win = win  # Хранение ссылки на объект окна
        self.scale = 1  # Начальный масштаб блока
        self.counter = 0  # Счётчик обновлений
        self.inc = 1  # Увеличение масштаба
        self.x = x  # Позиция блока по X
        self.y = y  # Позиция блока по Y
        self.max = max  # Максимальный масштаб блока
        
        # Загрузка и масштабирование изображения блока
        self.orig = pygame.image.load("Assets/block.jpeg")
        self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))
        self.rect = self.image.get_rect(center=(x, y))  # Получаем прямоугольник блока
        
    def update(self):
        # Обновление масштаба блока
        self.counter += 1
        if self.counter >= 2:  # Изменяем масштаб каждые 2 обновления
            self.scale += self.inc
            if self.scale <= 0 or self.scale >= self.max:
                self.inc *= -1  # Изменяем направление изменения масштаба
            self.image = pygame.transform.scale(self.orig, (self.scale, self.scale))  # Обновляем изображение
            self.rect = self.image.get_rect(center=(self.x, self.y))  # Обновляем прямоугольник
            self.counter = 0  # Сброс счётчика обновлений
            
        self.win.blit(self.image, self.rect)  # Отображение блока на экране


class ScoreCard:
    def __init__(self, x, y, win):
        # Инициализация счётчика очков
        self.win = win  # Хранение ссылки на объект окна
        self.size = 50  # Начальный размер шрифта
        self.inc = 1  # Изменение размера шрифта
        self.animate = False  # Анимация счётчика
        
        # Загрузка шрифта
        self.style = "Fonts/BubblegumSans-Regular.ttf"
        self.font = pygame.font.Font(self.style, self.size)

        # Рисование начального текста с нулевым счётом
        self.image = self.font.render("0", True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))  # Получаем прямоугольник для текста
        self.shadow_rect = self.image.get_rect(center=(x + 3, y + 3))  # Прямоугольник для тени текста
        
    def update(self, score):
        # Обновление отображаемого счёта
        if self.animate:  # Если активирована анимация
            self.size += self.inc  # Изменение размера шрифта
            self.font = pygame.font.Font(self.style, self.size)  # Обновление шрифта
            if self.size <= 50 or self.size >= 65:  # Проверка границ размера
                self.inc *= -1  # Изменение направления анимации
                
            if self.size == 50:  # Остановка анимации
                self.animate = False
        self.image = self.font.render(f"{score}", False, (255, 255, 255))  # Рисование текущего счёта
        shadow = self.font.render(f"{score}", True, (54, 69, 79))  # Рисование тени текста
        
        # Отображение тени и текста счётчика на экране
        self.win.blit(shadow, self.shadow_rect)
        self.win.blit(self.image, self.rect)


class Message:
    def __init__(self, x, y, size, text, font, color, win):
        # Инициализация сообщения
        self.win = win  # Хранение ссылки на объект окна
        if not font:  # Проверка на наличие пользовательского шрифта
            self.font = pygame.font.SysFont("Verdana", size)  # Использовать системный шрифт
            anti_alias = True  # Включение сглаживания
        else:
            self.font = pygame.font.Font(font, size)  # Используем пользовательский шрифт
            anti_alias = False  # Отключение сглаживания
        self.image = self.font.render(text, anti_alias, color)  # Рисуем текст
        self.rect = self.image.get_rect(center=(x, y))  # Получаем прямоугольник для текста
        self.shadow = self.font.render(text, anti_alias, (54, 69, 79))  # Рисуем тень текста
        self.shadow_rect = self.image.get_rect(center=(x + 2, y + 2))  # Прямоугольник для тени
        
    def update(self):
        # Отображение тени и текстового сообщения на экране
        self.win.blit(self.shadow, self.shadow_rect)
        self.win.blit(self.image, self.rect)


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, win):
        # Инициализация частицы
        super(Particle, self).__init__()
        self.x = x  # Позиция частицы по X
        self.y = y  # Позиция частицы по Y
        self.color = color  # Цвет частицы
        self.win = win  # Хранение ссылки на объект окна
        self.size = random.randint(4, 7)  # Случайный размер частицы
        if size == 0:
            xr = (-1, 2)  # Диапазон для случайного изменения скорости X
            yr = (-2, 2)  # Диапазон для случайного изменения скорости Y
            f = 1  # Множитель скорости
            self.life = 60  # Жизнь частицы
        elif size == 1:
            xr = (-3, 3)
            yr = (-6, 6)
            f = 2
            self.life = 60
        elif size == 2:
            xr = (-3, 3)
            yr = (-3, 3)
            f = 2
            self.life = 40

        self.x_vel = random.randrange(xr[0], xr[1]) * f  # Скорость частицы по X
        self.y_vel = random.randrange(yr[0], yr[1]) * f  # Скорость частицы по Y
        self.lifetime = 0  # Счётчик жизней частицы
            
    def update(self):
        # Обновление состояния частицы
        self.size -= 0.1  # Уменьшение размера частицы
        self.lifetime += 1  # Увеличение времени жизни
        if self.lifetime <= self.life:  # Если частица всё ещё жива
            self.x += self.x_vel  # Обновление позиции по X
            self.y += self.y_vel  # Обновление позиции по Y
            s = int(self.size)  # Преобразование размера в целое число
            pygame.draw.rect(self.win, self.color, (self.x, self.y, s, s))  # Отображение частицы
        else:
            self.kill()  # Удаление частицы после её жизни


def generate_particles(p, particles, color, win):
    # Генерация новых частиц
    particle_pos = list(p.rect.center)  # Получаем центр игрока
    particle_pos[1] += 25  # Сдвигаем центр для создания частиц снизу игрока

    # Добавление новой частицы в список частиц
    particles.append([particle_pos, [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 8)])
    for particle in particles:
        # Обновление позиции каждой частицы
        particle[0][0] -= particle[1][0]
        particle[0][1] -= particle[1][1]
        particle[2] -= 0.1  # Уменьшение размера частицы
        pygame.draw.circle(win, color, particle[0], int(particle[2]))  # Отрисовка частицы как круга
        # Проверка на удаление частицы при исчезновении
        if particle[2] <= 0:
            particles.remove(particle)

    return particles  # Возвращаем обновлённый список частиц