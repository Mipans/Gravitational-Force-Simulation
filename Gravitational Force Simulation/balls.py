import pygame, math
pygame.init()

WIDTH, HEIGHT = (1500, 775)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

BLACK, WHITE = (0, 0, 0), (255, 255, 255)


FPS = 60


class Ball():
    G = 30
    SCALE = 10
    TIMESTEP = 0.1

    def __init__(self, x, y, radious, colour, mass):
        self.x = x
        self.y = y
        self.radious = radious
        self.colour = colour
        self.mass = mass    # in kilograms

        self.orbit = []

        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH // 2
        y = self.y * self.SCALE + HEIGHT // 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH // 2
                y = y * self.SCALE + HEIGHT // 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.colour, False, updated_points)

        pygame.draw.circle(win, self.colour, (x, y), self.radious)
    
    def attarction(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = math.sqrt(distance_x**2 + distance_y**2)

        force = self.G * self.mass * other.mass / distance**2
        angle = math.atan2(distance_y, distance_x)
        force_x = math.cos(angle) * force
        force_y = math.sin(angle) * force
        return force_x, force_y
    
    def update_position(self, balls):
        total_fx, total_fy = 0, 0
        for ball in balls:
            if self == ball:
                continue

            fx, fy = self.attarction(ball)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx * self.TIMESTEP / self.mass
        self.y_vel += total_fy * self.TIMESTEP / self.mass

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def draw_window(balls):
    WIN.fill(BLACK)

    for planet in balls:
        planet.update_position(balls)
        planet.draw(WIN)

    pygame.display.update()



def main():
    run = True
    clock = pygame.time.Clock()

    red = Ball(15, 0, 5, (255, 50, 50), 120)
    red.y_vel = 10

    blue = Ball(-15, 0, 5, (50, 100, 255), 120)
    blue.y_vel = -10

    balls = [red, blue]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False

        draw_window(balls)

    pygame.quit()


if __name__ == '__main__':
    main()
