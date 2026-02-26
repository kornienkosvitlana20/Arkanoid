class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = 5
        self.speed_y = -5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def bounce_y(self):
        self.speed_y *= -1

    def bounce_x(self):
        self.speed_x *= -1
