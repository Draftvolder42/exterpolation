import math as m

class Radar:
    def __init__(self, x, y, angle, lock_distance, sweep_speed):
        self.x = x
        self.y = y
        self.x1 = 0
        self.y1 = 0
        self.angle = angle
        self.sweep_speed = sweep_speed
        self.lock_distance = lock_distance

    def _rotate2d(self, length, angle):
        """Вычисляет новую позицию на основе длины и угла."""
        return length * m.cos(angle) + self.x, length * m.sin(angle) + self.y

    def rotate_radar(self):
        """Поворачивает радар и обновляет конечную точку."""
        self.angle += self.sweep_speed
        self.x1, self.y1 = self._rotate2d(self.lock_distance, self.angle)

    def radar_lock(self, x, y):
        """Проверяет, находится ли точка (x, y) в пределах захвата радара."""
        for distance in range(1, self.lock_distance):
            x1, y1 = self._rotate2d(distance, self.angle)
            if m.fabs(x1 - x) < 20 and m.fabs(y1 - y) < 20:
                return True
        return False
