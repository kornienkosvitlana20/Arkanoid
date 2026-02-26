
import pygame


class Block:
    """
    Блок на ігровому полі.
    
    Чим відрізняється від Brick (файл партнера)?
    - Brick  = логіка (чи живий блок, скільки очок)
    - Block  = візуалізація (як малювати, анімація, ефекти)
    
    Ці два класи працюють разом.
    """

    # Константи анімації руйнування
    EXPLOSION_DURATION = 18   # кадрів живе анімація (при 60fps = 0.3 секунди)

    def __init__(self, x: int, y: int, width: int, height: int,
                 color: tuple, points: int):
        """
        x, y     — позиція блоку на екрані
        width    — ширина
        height   — висота
        color    — колір (RGB, наприклад (255, 50, 50))
        points   — скільки очок дає цей блок
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.points = points
        self.alive = True          

        #Анімація руйнування 
        self.exploding = False          
        self.explosion_timer = 0       
        self.explosion_particles = []   


    def hit(self):
        """
        Викликається коли м'яч влучає в блок.
        Запускає анімацію та позначає блок як знищений.
        """
        if not self.alive:
            return
        self.alive = False
        self.exploding = True
        self.explosion_timer = self.EXPLOSION_DURATION
        self._create_particles()

    def update(self):
        """
        Оновлення стану блоку кожен кадр.
        Потрібно викликати з game.py в ігровому циклі.
        """
        if self.exploding:
            self.explosion_timer -= 1
            # Рухаємо частинки
            for p in self.explosion_particles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.3        # гравітація
                p["alpha"] = int(255 * self.explosion_timer / self.EXPLOSION_DURATION)
            if self.explosion_timer <= 0:
                self.exploding = False

    def draw(self, surface: pygame.Surface):
        """
        Малює блок або анімацію руйнування на поверхні.
        """
        if self.alive:
            self._draw_block(surface)
        elif self.exploding:
            self._draw_explosion(surface)

    def is_done(self) -> bool:
        """
        Повертає True якщо блок знищено І анімація завершена.
        Використовується щоб прибрати блок зі списку.
        """
        return not self.alive and not self.exploding


    def _draw_block(self, surface: pygame.Surface):
        """Малює живий блок із градієнтом та бликом."""
        # Основний прямокутник
        pygame.draw.rect(surface, self.color, self.rect, border_radius=5)

        # Темна рамка навколо
        pygame.draw.rect(surface, (0, 0, 0), self.rect, width=1, border_radius=5)

        # Блик зверху (світла смужка — ефект об'єму)
        lighter = tuple(min(255, c + 90) for c in self.color)
        highlight = pygame.Rect(
            self.rect.x + 4,
            self.rect.y + 3,
            self.rect.width - 8,
            max(3, self.rect.height // 4)
        )
        pygame.draw.rect(surface, lighter, highlight, border_radius=3)

        # Темна смужка знизу (тінь)
        darker = tuple(max(0, c - 60) for c in self.color)
        shadow = pygame.Rect(
            self.rect.x + 4,
            self.rect.bottom - 5,
            self.rect.width - 8,
            3
        )
        pygame.draw.rect(surface, darker, shadow, border_radius=2)

    def _draw_explosion(self, surface: pygame.Surface):
        """Малює частинки вибуху при руйнуванні блоку."""
        for p in self.explosion_particles:
            alpha = max(0, min(255, p["alpha"]))
            size = max(1, p["size"])
            # Створюємо маленьку поверхню з прозорістю
            part_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = (*p["color"], alpha)
            pygame.draw.circle(part_surf, color_with_alpha, (size, size), size)
            surface.blit(part_surf, (int(p["x"]) - size, int(p["y"]) - size))

    def _create_particles(self):
        """Генерує частинки вибуху при знищенні блоку."""
        import random
        self.explosion_particles = []
        cx = self.rect.centerx
        cy = self.rect.centery

        for _ in range(12):   
            # Варіації кольору — трохи світліше або темніше основного
            variation = random.randint(-40, 40)
            color = tuple(max(0, min(255, c + variation)) for c in self.color)

            self.explosion_particles.append({
                "x": float(cx),
                "y": float(cy),
                "vx": random.uniform(-3.5, 3.5),   # горизонтальна швидкість
                "vy": random.uniform(-4.0, -0.5),   # вертикальна (вгору)
                "size": random.randint(2, 5),
                "color": color,
                "alpha": 255,
            })