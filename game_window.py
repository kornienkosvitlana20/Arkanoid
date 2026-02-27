import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS


class GameWindow:
    """
    Керує вікном pygame та фоновою анімацією.

    Що робить цей клас:
    - Створює вікно гри потрібного розміру
    - Малює анімований фон (зірки)
    - Контролює частоту кадрів (FPS)
    - Дає доступ до поверхні екрану для інших класів
    """

    def __init__(self, bg_color: tuple = (10, 10, 30)):
        """
        bg_color — колір фону (RGB), передається з main.py
        """
        # Ініціалізація pygame (якщо ще не ініціалізований)
        if not pygame.get_init():
            pygame.init()
        # Створення вікна
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)   # назва у заголовку вікна

        # Іконка вікна (проста — намальована програмно)
        icon = self._make_icon()
        pygame.display.set_icon(icon)

        self.clock = pygame.time.Clock()    # для контролю FPS
        self.bg_color = bg_color

        # Зірки на фоні — генеруємо один раз
        self.stars = self._generate_stars(80)

    def get_surface(self) -> pygame.Surface:
        """Повертає поверхню екрану. Інші класи малюють на ній."""
        return self.screen

    def clear(self):
        """
        Очищає екран перед малюванням нового кадру.
        Викликати на початку кожного кадру.
        """
        self.screen.fill(self.bg_color)
        self._draw_stars()

    def flip(self):
        """
        Оновлює екран (показує намальований кадр гравцю).
        Викликати в кінці кожного кадру.
        """
        pygame.display.flip()

    def tick(self):
        """Обмежує швидкість до FPS кадрів на секунду."""
        self.clock.tick(FPS)

    def draw_grid(self):
        """
        Малює тонку сітку на фоні — опціональний декоративний елемент.
        """
        grid_color = tuple(min(255, c + 15) for c in self.bg_color)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, grid_color, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, grid_color, (0, y), (SCREEN_WIDTH, y), 1)

    def _generate_stars(self, count: int) -> list:
        """Генерує список зірок для фонової анімації."""
        stars = []
        for _ in range(count):
            stars.append({
                "x": random.randint(0, SCREEN_WIDTH),
                "y": random.randint(0, SCREEN_HEIGHT),
                "size": random.randint(1, 3),
                # Яскравість — від тьмяної до яскравої
                "brightness": random.randint(80, 220),
                # Швидкість мерехтіння
                "twinkle_speed": random.uniform(0.02, 0.08),
                "twinkle_offset": random.uniform(0, 6.28),  # зсув фази
            })
        return stars

    def _draw_stars(self):
        """Малює мерехтливі зірки на фоні."""
        import math
        time_ms = pygame.time.get_ticks() / 1000.0   # секунди від старту

        for star in self.stars:
            # Мерехтіння через синус
            twinkle = math.sin(time_ms * star["twinkle_speed"] * 10 + star["twinkle_offset"])
            brightness = int(star["brightness"] + twinkle * 40)
            brightness = max(40, min(255, brightness))

            color = (brightness, brightness, brightness)
            pygame.draw.circle(
                self.screen,
                color,
                (star["x"], star["y"]),
                star["size"]
            )

    def _make_icon(self) -> pygame.Surface:
        """Створює просту іконку для вікна (кольоровий квадратик)."""
        icon = pygame.Surface((32, 32))
        icon.fill((10, 10, 30))
        pygame.draw.rect(icon, (0, 220, 220), (4, 20, 24, 6), border_radius=2)   # платформа
        pygame.draw.circle(icon, (255, 255, 255), (16, 14), 4)                    # м'яч
        pygame.draw.rect(icon, (220, 50, 50), (2, 4, 8, 4), border_radius=1)     # блок
        pygame.draw.rect(icon, (255, 165, 0), (12, 4, 8, 4), border_radius=1)
        pygame.draw.rect(icon, (50, 200, 50), (22, 4, 8, 4), border_radius=1)
        return icon