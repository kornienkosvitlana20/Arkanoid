class Ball:
    def __init__(self, x, y):
        # Початкові координати та фізичні параметри м'яча
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        # Оновлення позиції м'яча на кожному кадрі гри
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce_y(self):
        # Реверс швидкості по вертикалі при зіткненні
        self.speed_y *= -1

    def bounce_x(self):
        # Реверс швидкості по горизонталі при зіткненні
        self.speed_x *= -1
