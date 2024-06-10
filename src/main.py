import pygame
import math as m
import vec
import radar
import interface
import config
# Константы
pi = m.pi
tau = pi * 2
cos = m.cos
sin = m.sin

# Настройки
EXIT = False
FPS = config.FPS
WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
CENTER_WIDTH = WIDTH // 2
CENTER_HEIGHT = HEIGHT // 2

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def clamp(value, min_value, max_value):
    """Ограничение значения в заданном диапазоне"""
    return max(min(value, max_value), min_value)

def draw_points(points):
    """Рисование точек на экране"""
    for point in points:
        pygame.draw.circle(screen, (255, 255, 255), point, 10)

def round_to_precision(x, precision):
    """Округление числа до заданной точности"""
    return ((x * 10**precision) // 1) / 10**precision

# Параметры смещения и шрифты
x_offset = 0
y_offset = 0
a_offset = 0
font = pygame.font.SysFont(None, 50)

# Инициализация углов и цветов
old_angle = 0
angle2 = 0
current_angle = 0
color = (100, 0, 0)

# Создание объектов
vector = vec.Vector(CENTER_WIDTH, CENTER_HEIGHT, 15, 0)
radar = radar.Radar(CENTER_WIDTH, CENTER_HEIGHT, 0, 800, 0.09)
points = []
button = interface.ButtonMode()
color_change_counter = 0

while not EXIT:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            EXIT = True
    
    screen.fill((0, 0, 0))
    
    # Обработка ввода пользователя
    if keys[pygame.K_d]:
        vector.rotate_vector(0.3)
    if keys[pygame.K_a]:
        vector.rotate_vector(-0.3)
    if keys[pygame.K_s]:
        y_offset -= 0.0001
    if keys[pygame.K_w]:
        y_offset += 0.0001
    if keys[pygame.K_q]:
        a_offset -= 0.005
    if keys[pygame.K_e]:
        a_offset += 0.005

    vector.move_vector(0.5)
    radar.rotate_radar()

    if button.toggle_to_push(radar.radar_lock(vector.x1, vector.y1)):
        locked = True
        pygame.draw.circle(screen, (0, 255, 0), (vector.x1, vector.y1), 15)
        if len(points) >= 3:
            points.pop(0)
        points.append((vector.x1, vector.y1))
    else:
        locked = False
        pygame.draw.circle(screen, (255, 0, 0), (vector.x1, vector.y1), 15)

    draw_points(points)

    if len(points) >= 3:
        dist = m.sqrt((points[0][0] - points[1][0]) ** 2 + (points[0][1] - points[1][1]) ** 2)
        vec_a = [points[1][0] - points[0][0], points[1][1] - points[0][1]]
        vec_b = [points[1][0] - points[2][0], points[1][1] - points[2][1]]
        dist_b = m.sqrt(vec_b[0]**2 + vec_b[1]**2)

        offset_angle = m.atan2(vec_a[1], vec_a[0])
        offset_angle2 = m.atan2(vec_b[1], vec_b[0])
        ang_diff = ((m.pi - offset_angle) - (m.pi - offset_angle2))
        current_angle = offset_angle2 + ang_diff

        if m.fabs(m.fabs(ang_diff) - m.fabs(old_angle)) > 0.1:
            color = (255, 0, 0)
            color_change_counter = 0
            angle2 = (offset_angle2 - (old_angle - ang_diff)) + m.pi
        else:
            if color_change_counter < 100:
                color_change_counter += 1
            else:
                color = (100, 0, 0)
        old_angle = ang_diff

        pygame.draw.line(screen, color, (points[2][0], points[2][1]), 
                         (cos(angle2) * dist_b + points[2][0], sin(angle2) * dist_b + points[2][1]), 3)
        pygame.draw.line(screen, (0, 255, 0), (points[2][0], points[2][1]), 
                         (cos(current_angle) * dist_b + points[2][0], sin(current_angle) * dist_b + points[2][1]), 3)
    
    pygame.draw.line(screen, (0, 255, 0), (vector.x1, vector.y1), (vector.x2, vector.y2), 3)
    pygame.draw.line(screen, (0, 100, 0), (radar.x, radar.y), (radar.x1, radar.y1), 6)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
