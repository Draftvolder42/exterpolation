import math as m
import random

def noise(x, dist, gain=5000):
    """Добавляет случайный шум к значению x в пределах dist/gain."""
    return x + random.randint(-dist // gain, dist // gain)

def cl(x, xmin, xmax):
    """Ограничивает значение x в диапазоне от xmin до xmax."""
    return max(min(x, xmax), xmin)

def thr(x, minx, maxx):
    """Проверяет, находится ли x в диапазоне от minx до maxx."""
    return minx < x < maxx

def sgn(x):
    """Возвращает знак числа."""
    try:
        return abs(x) / x
    except ZeroDivisionError:
        return 1

def degrees_to_radians(deg):
    """Конвертирует градусы в радианы."""
    return deg * (m.pi / 180)

class Vector:
    def __init__(self, x, y, length, angle):
        self.x = x
        self.y = y
        self.length = length
        self.angle = degrees_to_radians(angle)
        
        self.x1 = x
        self.y1 = y
        self.x2 = 0
        self.y2 = 0
        
        self.l = length
        self.a = degrees_to_radians(angle)
        self.lock = False
        
        self.pi = m.pi
        self.tau = self.pi * 2

        self._d = 0
        self.h = 0

    def __len__(self):
        """Возвращает длину вектора."""
        return m.sqrt((self.x1 - self.x2) ** 2 + (self.y1 - self.y2) ** 2)

    def __repr__(self):
        """Возвращает строковое представление вектора."""
        return (f"x1 = {self.x1}; y1 = {self.y1}; x2 = {self.x2}; y2 = {self.y2}; "
                f"angle = {self.angle}; length = {self.length}; lock = {self.lock}")

    def __mul__(self, other):
        """Возвращает скалярное произведение двух векторов."""
        return ((self.x2 - self.x1) * (other.x2 - other.x1) +
                (self.y2 - self.y1) * (other.y2 - other.y1))

    def __eq__(self, other):
        """Проверяет равенство векторов."""
        if isinstance(other, Vector):
            return (self.x1 == other.x1 and 
                    self.y1 == other.y1 and 
                    self.x2 == other.x2 and 
                    self.y2 == other.y2)
        return (self.x1 == other and 
                self.y1 == other and 
                self.x2 == other and 
                self.y2 == other)

    def __gt__(self, other):
        """Проверяет, больше ли координата вектора, чем у другого."""
        return (self.x1 > other or self.y1 > other or
                self.x2 > other or self.y2 > other)

    def __lt__(self, other):
        """Проверяет, меньше ли координата вектора, чем у другого."""
        return (self.x1 < other or self.y1 < other or
                self.x2 < other or self.y2 < other)

    def __sub__(self, other):
        """Возвращает максимальную разницу между координатами двух векторов."""
        return max(abs(self.x1 - other.x1), abs(self.y1 - other.y1))

    def _rotate2D(self, length, angle):
        """Вычисляет новые координаты после поворота на заданный угол."""
        return (length * m.cos(angle) + self.x1,
                length * m.sin(angle) + self.y1)

    def move_vector(self, count):
        """Перемещает вектор на заданное количество единиц."""
        self.x1, self.y1 = self._rotate2D(count, self.angle)
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    def rotate_vector(self, angle):
        """Поворачивает вектор на заданный угол."""
        self.angle += degrees_to_radians(angle)
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    def reset(self):
        """Сбрасывает вектор к исходным координатам и параметрам."""
        self.x1 = self.x
        self.y1 = self.y
        self.length = self.l
        self.angle = self.a
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    def pn(self, vector, maneuverability):
        """Пропорциональная навигация."""
        dx = self.x1 - vector.x1
        dy = self.y1 - vector.y1
        g = m.sqrt(dx**2 + dy**2) if self.lock else 7000 + m.sqrt(dx**2 + dy**2)
        dx = noise(dx, g)
        dy = noise(dy, g)
        angle = m.atan2(dy, dx)
        dhor = angle - self._d
        self.h += dhor
        self._d = angle
        self.angle += cl(dhor * maneuverability, -0.044, 0.044)
        self.x2, self.y2 = self._rotate2D(self.length, self.angle)

    def check_in_field(self, vector, sector, range_):
        """Проверяет, находится ли точка в секторе и радиусе действия вектора."""
        dx = self.x1 - vector.x1
        dy = self.y1 - vector.y1
        angle = m.atan2(dy, dx)
        local_angle = m.atan2(self.y1 - self.y2, self.x1 - self.x2)

        if (thr(angle, local_angle - degrees_to_radians(sector), 
                local_angle + degrees_to_radians(sector)) and 
            m.sqrt((vector.x1 - self.x1) ** 2 + (vector.y1 - self.y1) ** 2) < range_):
            self.lock = True
        else:
            self.lock = False
