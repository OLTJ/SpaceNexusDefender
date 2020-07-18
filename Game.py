import pygame
import math
import random
import time
import numpy as np

class Player:
    def __init__(self, Position, Dimensions, Velocity, Color):
        self.Position = Position
        self.Dimensions = Dimensions
        self.Velocity = Velocity
        self.Color = Color
        self.Image = pygame.image.load('Player.png')

        self.BulletCount = 1

    def mouseControls(self):
        MousePosition = pygame.mouse.get_pos()
        MouseAction = pygame.mouse.get_pressed()
        if MouseAction[0] and len(Bullets) < 50:
            Bullets.append(Projectile([self.Position[0] + (self.Dimensions[0] // 2), self.Position[1] + (self.Dimensions[1] // 2)],
                [10, 10], self.Color, Vector2D([self.Position[0] + self.Dimensions[0] // 2, self.Position[1] + self.Dimensions[1] // 2], MousePosition)))

    def keyboardControls(self):
        Keyboard = pygame.key.get_pressed()
        DiagonalMultiplier = (1 / math.sqrt(2))
        if Keyboard[pygame.K_w] and 0 < self.Position[1]:
            if Keyboard[pygame.K_a] and 0 < self.Position[0]:
                self.Position[0] -= self.Velocity * DiagonalMultiplier
                self.Position[1] -= self.Velocity * DiagonalMultiplier
            elif Keyboard[pygame.K_d] and (self.Position[0] + self.Dimensions[0]) < WindowSize[0]:
                self.Position[0] += self.Velocity * DiagonalMultiplier
                self.Position[1] -= self.Velocity * DiagonalMultiplier
            else:
                self.Position[1] -= self.Velocity
        elif Keyboard[pygame.K_s] and (self.Position[1] + self.Dimensions[1]) < WindowSize[1]:
            if Keyboard[pygame.K_a] and 0 < self.Position[0]:
                self.Position[1] += self.Velocity * DiagonalMultiplier
                self.Position[0] -= self.Velocity * DiagonalMultiplier
            elif Keyboard[pygame.K_d] and (self.Position[0] + self.Dimensions[0]) < WindowSize[0]:
                self.Position[1] += self.Velocity * DiagonalMultiplier
                self.Position[0] += self.Velocity * DiagonalMultiplier
            else:
                self.Position[1] += self.Velocity
        elif Keyboard[pygame.K_a] and 0 < self.Position[0]:
            self.Position[0] -= self.Velocity
        elif Keyboard[pygame.K_d] and (self.Position[0] + self.Dimensions[0]) < WindowSize[0]:
            self.Position[0] += self.Velocity

        if Keyboard[pygame.K_SPACE]:
            Bullets.clear()
            Entities.clear()
            Particles.clear()

    def render(self, Window):
        Image = pygame.transform.scale(self.Image, (self.Dimensions))
        Image.set_colorkey((255,255,255))
        Window.blit(Image, self.Position)
        #pygame.draw.rect(Window, self.Color, [self.Position[0], self.Position[1], self.Dimensions[0], self.Dimensions[1]])

class Goal:
    def __init__(self, Position, Dimensions, Color):
        self.Position = Position
        self.Dimensions = Dimensions
        self.Color = Color
        self.Image = pygame.image.load('CRYSTAL.png')

        self.Health = 3
        self.Expiration = 0

    def animation(self):
        Animation = Randomize(0, 2)
        if Animation == 1:
            self.Position[0] -= 5
            self.Position[1] += 5
        elif Animation == 0:
            self.Position[0] += 5
            self.Position[1] -= 5

    def resetAnimation(self):
        if self.Expiration == 36:
            self.Position[0] = (WindowSize[0] // 2) - 100
            self.Position[1] = (WindowSize[1] // 2) - 100
            self.Expiration = 0
        self.Expiration += 1

    def render(self, Window):
        #Draw Image
        Image = pygame.transform.scale(self.Image, (200, 200))
        Window.blit(Image, self.Position)

        #Health Bar
        Font = pygame.font.SysFont(None, 30)
        Text = Font.render("HP: " + str(self.Health), True, (0,0,0))
        Window.blit(Text, (self.Position[0] + (self.Dimensions[0] // 2) - (Text.get_width() // 2), self.Position[1] + (self.Dimensions[0] // 2)- (Text.get_height() // 2)))

class Object:
    def __init__(self, Position, Dimensions, Color, Velocity, Damage, Health):
        self.Position = Position
        self.Dimensions = Dimensions
        self.Color = Color
        self.Velocity = Velocity
        self.Image = pygame.image.load('Enemy.png')

        self.Damage = Damage
        self.Health = Health

    def movement(self):
        Vector = Vector2D(Entity.Position, Crystal.Position)
        Entity.Position[0] -= Vector[0] * self.Velocity
        Entity.Position[1] -= Vector[1] * self.Velocity

    def render(self, Window):
        Image = pygame.transform.scale(self.Image, (50, 50))
        Image.set_colorkey((255,255,255))
        Window.blit(Image, self.Position)
        #pygame.draw.rect(Window, self.Color, [self.Position, self.Dimensions])

class Particle:
    def __init__(self, Position, Color, Direction):
        self.Position = Position
        self.Dimensions = [random.randrange(15, 20), random.randrange(15, 20)]
        self.Color = Color
        self.Velocity = 5
        self.Direction = Direction

        self.Expiration = 0

    def animation(self, Target):
        try:
            self.Dimensions[0] -= 0.25
            self.Dimensions[1] -= 0.25
            self.Position[0] += self.Direction[0] * self.Velocity
            self.Position[1] += self.Direction[1] * self.Velocity
        except:
            pass

    def tracking(self):
        if self.Dimensions[0] < 0 or self.Dimensions[1] < 0:
            Particles.pop(Particles.index(self))

    def render(self, Window):
        pygame.draw.rect(Window, self.Color, [self.Position, self.Dimensions])

class Projectile:
    def __init__(self, Position, Dimensions, Color, Direction):
        self.Position = Position
        self.Dimensions = Dimensions
        self.Color = Color
        self.Velocity = 0.75
        self.Direction = Direction
        self.Image = pygame.image.load('Projectile.png')

    def movement(self):
        for Bullet in Bullets:
            Bullet.Position[0] -= Bullet.Direction[0] * self.Velocity
            Bullet.Position[1] -= Bullet.Direction[1] * self.Velocity

    def render(self, Window):
        Image = pygame.transform.scale(self.Image, (10, 10))
        Image.set_colorkey((255,255,255))
        Window.blit(Image, self.Position)
        #pygame.draw.rect(Window, self.Color, [self.Position, self.Dimensions])

def createEntities(numbOfEntities):
    if len(Entities) < numbOfEntities:
        angle = random.randint(0, int((10 - 1) / 0.1)) * 0.1 + 1
        Entities.append(Object([round(1000 * math.cos(angle) + Crystal.Position[0] + (Crystal.Dimensions[0] // 2)),
                        round(1000 * math.sin(angle) + Crystal.Position[1] + (Crystal.Dimensions[1] // 2))], [50, 50], (142,17,17), 0.5, 10, 1))

def createParticles(Entity, numbOfParticles):
    ColorVariety = lambda x: Randomize(200, x) if (x > 200) else x

    for i in range(numbOfParticles):
        Particles.append(Particle([Entity.Position[0] + (Entity.Dimensions[0] // 2) + Randomize(-50, 50),
                                   Entity.Position[1] + (Entity.Dimensions[1] // 2) + Randomize(-50, 50)],
                                  [ColorVariety(Entity.Color[0]), ColorVariety(Entity.Color[1]), ColorVariety(Entity.Color[2])], Vector2D(Entity.Position, [Entity.Position[0] + Randomize(-50, 50), Entity.Position[1] + Randomize(-50, 50)])))

def CollisionDetection(Entity1, Entity2):
    if Entity1.Position[1] < Entity2.Position[1] + Entity2.Dimensions[1] and Entity1.Position[1] + Entity1.Dimensions[1] > Entity2.Position[1]:
        if Entity1.Position[0] < Entity2.Position[0] + Entity2.Dimensions[0] and Entity1.Position[0] + Entity1.Dimensions[0] > Entity2.Position[0]:
            return True

def Vector2D(EntityPosition, TargetPosition):
    #try:
    #    Distance = [Entity.Position[0] - (Target.Position[0] + (Target.Dimensions[0] // 2)), Entity.Position[1] - (Target.Position[1] + (Target.Dimensions[1] // 2))]
    #    Normalize = math.sqrt(Distance[0] ** 2 + Distance[1] ** 2)
    #    Direction = [Distance[0] / Normalize, Distance[1] / Normalize]
    #    Vector = [Direction[0], Direction[1]]
    #    return Vector
    try:
        Distance = [EntityPosition[0] - TargetPosition[0], EntityPosition[1] - TargetPosition[1]]
        Normalize = math.sqrt(Distance[0] ** 2 + Distance[1] ** 2)
        Direction = [Distance[0] / Normalize, Distance[1] / Normalize]
        Vector = [Direction[0], Direction[1]]
        return Vector

    except ZeroDivisionError:
        pass

def Randomize(start, end):
    return random.randrange(start, end)

def developerPanel():
    Total = len(Entities) + len(Particles)
    Font = pygame.font.SysFont(None, 30)
    Text = Font.render("Entities: " + str(Total) + " Total Killed: " + str(TotalKilled), True, (0, 0, 0))
    Window.blit(Text, (5, 5))

def renderWindow():
    Window.fill((255,255,255))
    developerPanel()
    for Entity in Entities:
        Entity.render(Window)
    for Bullet in Bullets:
        Bullet.render(Window)
    for Dot in Particles:
        Dot.render(Window)
    Crystal.render(Window)
    Character.render(Window)
    pygame.display.update()

#Game Initialization
pygame.init()
Window = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
WindowSize = Window.get_size()
pygame.font.init()
Clock = pygame.time.Clock()

#Object Declaration
Character = Player([500, 500], [75, 75], 5, (255,0,150))
Crystal = Goal([(WindowSize[0] // 2) - 100, (WindowSize[1] // 2) - 100], [200, 200], (255, 0, 150))
Entities = []
Bullets = []
Particles = []

#Variable Declaration
StartTime = time.time()
TimeElapse = 0.0
TotalKilled = 0
numberOfEntities = 20
numberOfParticles = random.randrange(100, 200)

Running = True

while Running:
    Clock.tick(144)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    createEntities(numberOfEntities)

    for Entity in Entities:
        Entity.movement()
        if CollisionDetection(Entity, Crystal):
            Crystal.Health -= 1
            Crystal.animation()
            Entities.pop(Entities.index(Entity))
            createParticles(Crystal, numberOfParticles)
        for Bullet in Bullets:
            if CollisionDetection(Entity, Bullet):
                TotalKilled += 1
                createParticles(Entity, numberOfParticles)
                try:
                    Bullets.pop(Bullets.index(Bullet))
                    Entities.pop(Entities.index(Entity))
                except ValueError:
                    pass

    for Dot in Particles:
        Dot.animation(Crystal)
        Dot.tracking()

    for Bullet in Bullets:
        if Bullet.Position[0] < 0 or Bullet.Position[1] < 0:
            Bullets.pop(Bullets.index(Bullet))
        elif Bullet.Position[0] + Bullet.Dimensions[0] > WindowSize[0] or Bullet.Position[1] + Bullet.Dimensions[1] > WindowSize[1]:
            Bullets.pop(Bullets.index(Bullet))
        Bullet.movement()

    Crystal.resetAnimation()
    Character.keyboardControls()
    Character.mouseControls()

    renderWindow()
pygame.quit()