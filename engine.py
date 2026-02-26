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

class Paddle:
    def __init__(self, x, y):
        # Параметри ракетки: ширина, висота та початкові координати
        self.width = 100
        self.height = 15
        self.x = x
        self.y = y
        self.speed = 10

    def move_left(self):
        # Рух вліво (обмеження x > 0 додасть напарниця в головному циклі або додамо пізніше)
        if self.x > 0:
            self.x -= self.speed

    def move_right(self, screen_width):
        # Рух вправо з урахуванням ширини вікна
        if self.x < screen_width - self.width:
            self.x += self.speed

class PhysicsManager:
    @staticmethod
    def check_wall_collision(ball, screen_width):
        # Відскок від лівої (0) та правої (screen_width) стін
        if ball.x - ball.radius <= 0 or ball.x + ball.radius >= screen_width:
            ball.bounce_x()
        
        # Відскок від верхньої стіни (стелі)
        if ball.y - ball.radius <= 0:
            ball.bounce_y()

    @staticmethod
    def is_ball_out(ball, screen_height):
        # Перевірка, чи м'яч не впав нижче ракетки
        return ball.y > screen_height

        @staticmethod
    def check_paddle_collision(ball, paddle):
        # Якщо м'яч торкається прямокутника ракетки
        if (paddle.x <= ball.x <= paddle.x + paddle.width and
            paddle.y <= ball.y + ball.radius <= paddle.y + paddle.height):
            ball.bounce_y()
            return True
        return False