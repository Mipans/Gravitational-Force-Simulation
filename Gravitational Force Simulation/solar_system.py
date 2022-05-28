import pygame, math
pygame.init()

WIDTH, HEIGHT = (800, 800)                                              # customiseable!!
WIN = pygame.display.set_mode((WIDTH*2, HEIGHT))
pygame.display.set_caption("Planet Simulation")

BLACK, WHITE, YELLOW = (0, 0, 0), (255, 255, 255), (255, 255, 0)


FPS = 60


class Planet():
    AU = 149.6e6 * 1000
    G = 6.67428e-11                                                     # customiseable!!
    SCALE = 250 / AU    # 1 AU = 100 pixels
    TIMESTEP = 3600*24  # 1 day is 1 second

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
    
    def update_position(self, planets):
        total_fx, total_fy = 0, 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attarction(planet)
            total_fx += fx
            total_fy += fy
        
        self.x_vel += total_fx * self.TIMESTEP / self.mass
        self.y_vel += total_fy * self.TIMESTEP / self.mass

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def draw_window(planets):
    WIN.fill(BLACK)

    for planet in planets:
        planet.update_position(planets)
        planet.draw(WIN)

    pygame.display.update()



def main():
    run = True
    clock = pygame.time.Clock()
                                                                        # customiseable from here . . .
    sun     = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10**30)
    sun.x_vel = 250

    mercury = Planet(-0.387*Planet.AU, 0, 4, (100, 100, 100), 3.285 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus   = Planet(-0.723*Planet.AU, 0, 6, (200, 170, 100), 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    earth   = Planet(-1*Planet.AU, 0, 6, (100, 100, 200), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars    = Planet(-1.523*Planet.AU, 0, 4, (200, 100, 100), 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, mercury, venus, earth, mars]
                                                                        # to here !!
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or (pygame.key.get_pressed()[pygame.K_ESCAPE]):
                run = False

        draw_window(planets)

    pygame.quit()


if __name__ == '__main__':
    main()
