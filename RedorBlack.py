import pygame,sys,random
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 10
CARDSIZE = 40
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHTBLUE = (135,206,250)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = DARKGRAY
CARDCOLOR = [RED, BLACK, GREEN]

class roulette():
    def __init__(self):
        self.health = 10
        self.chioce = 0
        self.point = 0
        self.fate = 0
        self.turns = 0
        self.mycard = []

    def showStartScreen(self):
        titleFont = pygame.font.Font('freesansbold.ttf', 50)
        titleSurf1 = titleFont.render('RED OR BLACK!', True, WHITE, DARKGRAY)

        while True:
            DISPLAYSURF.fill(BGCOLOR)
            rotatedSurf1 = pygame.transform.rotate(titleSurf1, 0)
            rotatedRect1 = rotatedSurf1.get_rect()
            rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
            DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

            self.drawPressKeyMsg()

            if self.checkForKeyPress():
                pygame.event.get() # clear event queue
                return
            pygame.display.update()

    def drawPressKeyMsg(self):
        pressKeySurf = PRESSFONT.render('Press a key to play.', True, BLACK)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (WINDOWWIDTH - WINDOWWIDTH/3, WINDOWHEIGHT - WINDOWHEIGHT/6)
        DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    def checkForKeyPress(self):
        if len(pygame.event.get(pygame.QUIT)) > 0:
            self.terminate()

        keyUpEvents = pygame.event.get(pygame.KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == pygame.K_ESCAPE:
            self.terminate()
        return keyUpEvents[0].key

    def terminate(self):
        pygame.quit()
        sys.exit()

    def showtime(self,stime,pfunc,*args,**kwargs):
        starttime = pygame.time.get_ticks()
        while True:
            pfunc(*args, **kwargs)
            time = (pygame.time.get_ticks()-starttime)/1000
            if time>stime:
                break

    def roulette(self):
        result = random.randint(0,1)
        self.fate = result

    def drawRob(self):
        # result = random.randint(0, 1)
        if self.fate:
            scoreSurf = BASICFONT.render('RED', True, RED)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft = (WINDOWWIDTH/3, WINDOWHEIGHT/3)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            # pygame.time.wait(1000)
        else:
            scoreSurf = BASICFONT.render('BLACK', True, BLACK)
            scoreRect = scoreSurf.get_rect()
            scoreRect.topleft = (WINDOWWIDTH/3, WINDOWHEIGHT/3)
            DISPLAYSURF.blit(scoreSurf, scoreRect)
            # pygame.time.wait(1000)
        pygame.display.update()


    def drawTable(self,TableCoord):
        x = TableCoord['x'] * CELLSIZE
        y = TableCoord['y'] * CELLSIZE
        width = WINDOWWIDTH/2
        height = WINDOWHEIGHT/4
        TableRect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(DISPLAYSURF, LIGHTBLUE, TableRect)

    def drawApple(self, coords):
        for coord in coords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, RED, appleRect)

    def drawGrid(self):
        for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
        for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
            pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

    def drawPoint(self):
        if self.point%2 != 0:
            x = int(WINDOWWIDTH/4 - 2*CELLSIZE)
            y = int(3*WINDOWHEIGHT/4)
            # width = WINDOWWIDTH/2
            # height = WINDOWHEIGHT/4
            # PointCircle = pygame.cir(x, y, width, height)
            pygame.draw.circle(DISPLAYSURF, DARKGREEN, (x,y),5,0)

    def sendcard(self):
        card = random.randint(0,2)
        if len(self.mycard) < 7:
            self.mycard.append(card)

    def usecard(self,usecard_index):
        if usecard_index is not None:
            usecard = self.mycard[usecard_index]
            self.mycard.remove(self.mycard[usecard_index])
            if usecard == 0:
                self.health += 1
            elif usecard == 1:
                self.health -= 1
            else:
                self.mycard.append(random.randint(0,2))
                self.mycard.append(random.randint(0, 2))
            if self.health == 0:
                self.terminate()
        return
    def get_usecardindex(self,mx,my,table):
        x0 = table['x'] * CELLSIZE + 2
        y0 = table['y'] * CELLSIZE + 2
        if x0 + (CARDSIZE+2)*len(self.mycard)> mx > x0 and y0 + CARDSIZE*1.5 > my > y0:
            return int((mx-x0)/(CARDSIZE+2))
        else:
            return None
    def get_apple(self,table):
        apple = []
        for i in range(self.health):
            apple.append({'x': table['x'] + i * 2, 'y': table['y'] - 2})
        return apple

    def drawCard(self,table):
        if self.mycard is not None:
            for i,card in enumerate(self.mycard):
                color = CARDCOLOR[card]
                x = table['x'] * CELLSIZE + 2 + (i) * (CARDSIZE+2)
                y = table['y'] * CELLSIZE + 2
                cardRect = pygame.Rect(x, y, CARDSIZE, CARDSIZE*1.5)
                pygame.draw.rect(DISPLAYSURF, color, cardRect)

    def step(self,table):
        if self.chioce == self.fate:
            self.point += 1
            if self.point%2 == 0:
                self.health += 1
        else:
            self.health -= 1
            self.sendcard()
            self.point = 0
        if self.health == 0:
            self.terminate()
        apple = self.get_apple(table)
        return apple


    def runGame(self):
        oldturns = 0
        table = {'x': CELLWIDTH/4, 'y': 3*CELLHEIGHT/4}
        apple = []
        for i in range(self.health):
            apple.append({'x': table['x']+i*2, 'y': table['y']-2})
        while True:
            oldturns = self.turns
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.chioce = 1
                    if event.key == pygame.K_b:
                        self.chioce = 0
                    self.turns += 1
                    self.roulette()
                elif event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = pygame.mouse.get_pos()
                        index = self.get_usecardindex(mx,my,table)
                        self.usecard(index)
                        apple = self.get_apple(table)
            DISPLAYSURF.fill(BGCOLOR)
            self.drawGrid()
            self.drawTable(table)
            self.drawApple(apple)
            self.drawPoint()
            self.drawCard(table)
            if self.turns>oldturns:
                # self.drawRob()
                self.showtime(1,self.drawRob)
                apple = self.step(table)
                # pygame.time.wait(500)
            pygame.display.update()
            FPSCLOCK.tick(FPS)


    def main(self):
        global FPSCLOCK, DISPLAYSURF, BASICFONT,PRESSFONT,CARDSIZE,CARDCOLOR

        pygame.init()
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
        PRESSFONT = pygame.font.Font('freesansbold.ttf', 16)
        BASICFONT = pygame.font.Font('freesansbold.ttf', 64)
        pygame.display.set_caption('RoB')

        self.showStartScreen()
        while True:
            self.runGame()



if __name__ == '__main__':
    rob = roulette()
    rob.main()