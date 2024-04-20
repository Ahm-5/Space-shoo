import pygame
import math
import random
import json

pygame.init()

sw = 800
sh = 800

bg = pygame.image.load("background.png")
asteroid50 = pygame.image.load("asteroid50.png")
asteroid100 = pygame.image.load("asteroid100.png")
asteroid150 = pygame.image.load("asteroid150.png")
player_ship = pygame.image.load("spaceship.png")
star_P = pygame.image.load("power.png")
extra_l = pygame.image.load("shield.png")
blast_P = pygame.image.load("blast.png")
score_P = pygame.image.load("score.png")

pygame.mixer.music.load("backgoundm.wav")
shoot = pygame.mixer.Sound("shoot.wav")
banglargesound = pygame.mixer.Sound("banglarge.wav")
bangsmallsound = pygame.mixer.Sound("bangsmall.wav")
collision = pygame.mixer.Sound("collison.wav")
powerup = pygame.mixer.Sound("powerup.wav")
shoot.set_volume(0.05)
banglargesound.set_volume(0.05)
bangsmallsound.set_volume(0.05)
powerup.set_volume(0.09)
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)


pygame.display.set_caption('Asteroids shooter')
win = pygame.display.set_mode((sw, sh))

clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0
highscore = 0 # Initialize highscore to 0
rapidfire = False
rfstart = -1
issoundon = True



class player(object):
    def __init__(self):
        self.image = player_ship
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.x = sw // 2
        self.y = sh // 2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w // 2, self.y - self.sine + self.h // 2)

    def draw(self, win):
        # win.blit(self.image, [self.x, self.y, self.w, self.h])
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnleft(self):
        self.angle += 5
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w // 2, self.y - self.sine * self.h // 2)

    def turnright(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w // 2, self.y - self.sine * self.h // 2)

    def moveforward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w // 2, self.y - self.sine * self.h // 2)

    def updatelocation(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

class bullet(object):
    def __init__(self):
        self.point = player1.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player1.cosine
        self.s = player1.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (255, 255, 0), [self.x, self.y, self.w, self.h])

    def checkoffscreen(self):
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return


class asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), random.choice([-1*self.h - 5, sh + 5])),(random.choice([-1*self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    @staticmethod
    def destroy_all():
        asteroids.clear()

    @staticmethod
    def multiply_score():
        global score
        score *= 2

class PowerLive(object):
    def __init__(self):
        self.image = extra_l
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),(random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Star(object):
    def __init__(self):
        self.image = star_P
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])), (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class BlastPowerup(object):
    def __init__(self):
        self.image = blast_P
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])), (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

class ScoreMultiplierPowerup(object):
    def __init__(self):
        self.image = score_P
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])),
                                       (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh - self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1

        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * 2
        self.yv = self.ydir * 2

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

def save_player_data(filename):
    data = {
        'lives': lives,
        'score': score,
        'highscore': highscore
    }
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_player_data(filename):
    global lives, score, highscore
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            lives = data['lives']
            score = data['score']
            highscore = data['highscore']
    except FileNotFoundError:
        # Handle the case where the file doesn't exist yet
        pass

def redrawGameWindow():
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont("Retronoid", 30)
    livestext = font.render("Lives: " + str(lives), 1, (255,20,147))
    playagaintext = font.render("Press R to play again", 1, (0,250,154))
    scoretext = font.render("Score: " + str(score), 1, (240,128,128))
    global highscore
    if score > highscore:
        highscore = score
    highscoretext = font.render("High Score: " + str(highscore), 1, (255,255,0))
    win.blit(highscoretext, (sw - highscoretext.get_width() - 25, 25))

    player1.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerbullets:
        b.draw(win)
    for s in stars:
        s.draw(win)
    for p in extralives:
        p.draw(win)
    for t in blast_powerups:
        t.draw(win)
    for m in score_multiplier_powerups:
        m.draw(win)

    if rapidfire:
        progress = min(1.0, (count - rfstart) / 500)
        width = int(100 - 100 * progress)
        pygame.draw.rect(win, (131, 111, 255), [sw // 2 - 51, 19, 102, 22])
        pygame.draw.rect(win, (176, 224, 230), [sw // 2 - 50, 20, width, 20])


    if gameover:
        win.blit(playagaintext, (sw//2-playagaintext.get_width()//2, sh//2 - playagaintext.get_height()//2))

    win.blit(scoretext, (sw - scoretext.get_width() - 60, 60))
    win.blit(livestext, (25,25))
    pygame.display.update()


player1 = player()
playerbullets = []
asteroids = []
count = 0
stars = []
extralives = []
blast_powerups = []
score_multiplier_powerups = []


run = True
while run:
    clock.tick(60)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3,])
            asteroids.append(asteroid(ran))
        if count % 500 == 0:
            stars.append(Star())

        if count % 1000 == 0:
            extralives.append(PowerLive())

        if count % 2000 == 0:
            blast_powerups.append(BlastPowerup())

        if count % 1500 == 0:
            score_multiplier_powerups.append(ScoreMultiplierPowerup())

        player1.updatelocation()
        for b in playerbullets:
            b.move()
            if b.checkoffscreen():
                playerbullets.pop(playerbullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            if (player1.x >= a.x and player1.x <= a.x + a.w) or (player1.x + player1.w >= a.x and player1.x + player1.w <= a.x +a.w):
                if (player1.y >= a.y and player1.y <= a.y + a.h) or (player1.y +player1.h >= a.y and player1.y + player1.h <= a.y + a.h):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    if issoundon:
                        collision.play()
                    break



            # bullet detection
            for b in playerbullets:
                if (b.x >= a.x and b.x <= a.x + a.x + a.w) or b.x + b.w >= a.x and b.x + b.w <= a.x + a.x + a.w:
                    if (b.y >= a.y and b.y <= a.y + a.h) or b.y + b.h >= a.y and b.y + b.h <=a.y + a.h:
                        if a.rank == 3:
                            if issoundon:
                                banglargesound.play()
                            score += 10
                            na1 = asteroid(2)
                            na2 = asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            if issoundon:
                                bangsmallsound.play()
                            score += 20
                            na1 = asteroid(1)
                            na2 = asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            if issoundon:
                                bangsmallsound.play()
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        playerbullets.pop(playerbullets.index(b))
                        break

        for s in stars:
            s.x += s.xv
            s.y += s.yv
            if s.x < -100 - s.w or s.x > sw + 100 or s.y > sh + 100 or s.y < -100 - s.h:
                stars.pop(stars.index(s))
                break
            for b in playerbullets:
                if (b.x >= s.x and b.x <= s.x + s.w) or b.x + b.w >= s.x and b.x + b.w <= s.x + s.w:
                    if (b.y >= s.y and b.y <= s.y + s.h) or b.y + b.h >= s.y and b.y + b.h <= s.y + s.h:
                        rapidfire = True
                        rfstart = count
                        stars.pop(stars.index(s))
                        playerbullets.pop(playerbullets.index(b))
                        if issoundon:
                            powerup.play()
                        break

        for p in extralives:
            p.x += p.xv
            p.y += p.yv
            if (player1.x >= p.x and player1.x <= p.x + p.w) or (player1.x + player1.w >= p.x and player1.x + player1.w <= p.x + p.w):
                if (player1.y >= p.y and player1.y <= p.y + p.h) or (player1.y + player1.h >= p.y and player1.y + player1.h <= p.y + p.h):
                    lives += 1
                    extralives.pop(extralives.index(p))
                    if issoundon:
                        powerup.play()
                    break
            for b in playerbullets:
                if (b.x >= p.x and b.x <= p.x + p.w) or b.x + b.w >= p.x and b.x + b.w <= p.x + p.w:
                    if (b.y >= p.y and b.y <= p.y + p.h) or b.y + b.h >= p.y and b.y + b.h <= p.y + p.h:
                        extralives.pop(extralives.index(p))
                        playerbullets.pop(playerbullets.index(b))
                        if issoundon:
                            powerup.play()
                        break

        for t in blast_powerups:
            t.x += t.xv
            t.y += t.yv
            if (player1.x >= t.x and player1.x <= t.x + t.w) or (player1.x + player1.w >= t.x and player1.x + player1.w <= t.x + t.w):
                if (player1.y >= t.y and player1.y <= t.y + t.h) or (player1.y + player1.h >= t.y and player1.y + player1.h <= t.y + t.h):
                    asteroid.destroy_all()
                    blast_powerups.pop(blast_powerups.index(t))
                    if issoundon:
                        powerup.play()
                    break

        for m in score_multiplier_powerups:
            m.x += m.xv
            m.y += m.yv
            if (player1.x >= m.x and player1.x <= m.x + m.w) or (player1.x + player1.w >= m.x and player1.x + player1.w <= m.x + m.w):
                if (player1.y >= m.y and player1.y <= m.y + m.h) or (player1.y + player1.h >= m.y and player1.y + player1.h <= m.y + m.h):
                    asteroid.multiply_score()
                    score_multiplier_powerups.pop(score_multiplier_powerups.index(m))
                    if issoundon:
                        powerup.play()
                    break

        if lives <= 0:
            gameover = True
            if score > highscore:
                highscore = score

        if rfstart != -1:
            if count - rfstart > 500:
                rapidfire = False
                rfstart = -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player1.turnleft()
        if keys[pygame.K_RIGHT]:
            player1.turnright()
        if keys[pygame.K_UP]:
            player1.moveforward()
        if keys[pygame.K_SPACE]:
            if rapidfire:
                playerbullets.append(bullet())
                if issoundon:
                    shoot.play()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                save_player_data('player_data.json')

            if event.key == pygame.K_l:
                load_player_data('player_data.json')

            if event.key == pygame.K_SPACE:
                if not gameover:
                    if not rapidfire:
                        playerbullets.append(bullet())
                        if issoundon:
                            shoot.play()

            if event.key == pygame.K_m:
                issoundon = not issoundon
            if event.key == pygame.K_r:
                if gameover:
                    gameover = False
                    lives = 3
                    score = 0
                    asteroids.clear()
                    stars.clear()


    redrawGameWindow()
pygame.quit()
