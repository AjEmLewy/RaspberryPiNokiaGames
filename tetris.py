import time, pygame, sys, random, json
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont
import Adafruit_Nokia_LCD as LCD

#TODO:
# SCORE // done - dodaj rysowanie
# czas  // done - dodaj rysowanie
# h-score na pewno
# check if koniec gry // done
# może jakaś muzyczka?
# wyswietlanie następnego klocka jaki będzie leciał
# zmiana poziomu trudnosci // done
# przerobic na wersję z 4 pixelami w wolnej chwili

PRAWY_LIMIT = 19
LEWY_LIMIT = 8
DOLNY_LIMIT = 16
class Tetris():
    def __init__(self, display, draw, image):
        self.display = display
        self.draw = draw
        self.image = image
        self.set_start_cond()
        self.klocek = self.wybor[random.randint(0,6)](self.draw, self.wyznaczniki, self.clearing_wyznaczniki)
        self.klocek.rysuj_punkty()
        self.gra()
        self.check_if_highscore()
    
    def __str__(self):
        return "\n".join([''.join(str(self.wyznaczniki[i])) for i in range(len(self.wyznaczniki))])

    def set_start_cond(self):
        self.clearing_wyznaczniki =[[0 for i in range(11)] for i in range(16)]
        self.wyznaczniki = []
        self.score = 0
        self.start_time = time.time()
        self.repeat_count = 5
        self.koniec = False
        self.wybor = [Tau,Kij,Kwadrat,L_normal,L_turned,
                      Z_normal,Z_turned]


    def gra(self):
        pygame.event.clear()
        while not self.koniec:
            for _ in range(self.repeat_count):
                smth = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            smth = self.klocek.move_left()
                        elif event.key == pygame.K_RIGHT:
                            smth = self.klocek.move_right()
                        elif event.key == pygame.K_z:
                            smth = self.klocek.switch_left()
                        elif event.key == pygame.K_x:
                            smth = self.klocek.switch_right()
                    pygame.event.clear()
                    if smth: self.rerysuj()
                time.sleep(0.1)
            #sprobuj ruszyc w dół
            if(not self.klocek.move_down()):
                self.klocek.append_to_wyznaczniki()
                self.clear_check()
                self.klocek = self.wybor[random.randint(0,6)](self.draw, self.wyznaczniki, self.clearing_wyznaczniki)
                if(self.check_if_koniec()): return
                self.klocek.rysuj_punkty()
                self.rerysuj()
            else:
                self.rerysuj()
            self.set_repeat_count()
        
    

############ CLEARING RZEDOW
    def rysuj_punkty(self):
        temp_pts = []
        for p in self.wyznaczniki:
            temp_pts += [(p[0]*3,p[1]*3), (p[0]*3+1,p[1]*3), (p[0]*3+2,p[1]*3),
                         (p[0]*3,p[1]*3+1), (p[0]*3+1,p[1]*3+1), (p[0]*3+2,p[1]*3+1),
                         (p[0]*3,p[1]*3+2), (p[0]*3+1,p[1]*3+2), (p[0]*3+2,p[1]*3+2)]
        self.draw.point(temp_pts, fill=0)

    def zmaz_punkt(self, p):
        temp_pts = []
        temp_pts += [(p[0]*3,p[1]*3), (p[0]*3+1,p[1]*3), (p[0]*3+2,p[1]*3),
                     (p[0]*3,p[1]*3+1), (p[0]*3+1,p[1]*3+1), (p[0]*3+2,p[1]*3+1),
                     (p[0]*3,p[1]*3+2), (p[0]*3+1,p[1]*3+2), (p[0]*3+2,p[1]*3+2)]
        self.draw.point(temp_pts, fill=255)

    def clear_check(self):
        cleared = False
        cleared_rows = []
        for num, rzad in enumerate(self.clearing_wyznaczniki):
            if all(rzad):
                self.remove_rzad(num)
                cleared = True
                cleared_rows.append(num)
        if cleared:
            for index in cleared_rows:
                self.add_score()
                for ind, wyzn in enumerate(self.wyznaczniki):
                    if wyzn[1]<index:
                        self.wyznaczniki[ind] = (wyzn[0],wyzn[1]+1)
            self.clear_rzedy(cleared_rows)
                    
    def remove_rzad(self, index):
        del(self.clearing_wyznaczniki[index])
        self.clearing_wyznaczniki.insert(0, [0 for _ in range(11)])
        for i in range(11):
            self.wyznaczniki.remove((i+LEWY_LIMIT, index))

    def clear_rzedy(self, indexy):
        for i in range(11):
            for index in indexy:
                self.zmaz_punkt((i+LEWY_LIMIT, index))
            self.display.image(self.image)
            self.display.display()
            time.sleep(0.06)
        self.rysuj_wyznaczniki()

############## KONIEC CLEARINGU

    def rysuj_wyznaczniki(self):
        self.draw.rectangle((LEWY_LIMIT*3-1,0,PRAWY_LIMIT*3, LCD.LCDHEIGHT-1), outline=0, fill=255)
        draw.line((LEWY_LIMIT*3,0,PRAWY_LIMIT*3-1,0),fill=255)
        draw.line((LEWY_LIMIT*3,47,PRAWY_LIMIT*3-1,47),fill=255)
        self.rysuj_punkty()
        self.display.image(self.image)
        self.display.display()

    def add_score(self):
        self.start_time+=int((time.time()-self.start_time)/6)

    def set_repeat_count(self):
        if time.time()-self.start_time < 60: return
        elif time.time()-self.start_time > 180: self.repeat_count = 3
        else: self.repeat_count = 4

    def check_if_koniec(self):
        for punkt in self.klocek.punkty:
            if punkt in self.wyznaczniki: return True
        return False

    def check_if_highscore(self):
        with open('highscores.json') as file:
            data = json.load(file)
        if self.score > int(data['tetris']):
            data['tetris'] = str(self.score)
            with open('highscores.json', 'w') as file:
                json.dump(data, file)
            self.wyswietl_highscore()

    def wyswietl_highscore(self):
        pass

    def rerysuj(self):
        self.display.image(self.image)
        self.display.display()



#########################  KLOCKI  ##############################
        
class Klocek():
    def __init__(self, draw, wyznaczniki, cw):
        #TODO: pamietaj o self.punkty w pochodnych
        self.draw = draw
        self.wyznaczniki = wyznaczniki
        self.clearing_wyznaczniki = cw
    
    def switch_right(self):
        pass
    
    def switch_left(self):
        pass

    def move_down(self):
        #check if can into space
        igreki = [x[1]-DOLNY_LIMIT+1 for x in self.punkty]
        if not all(igreki): return False

        #sprawdz czy nie kolajduje z innymi
        nowe_pkt=[]
        for punkt in self.punkty:
            nowe_pkt.append((punkt[0], punkt[1]+1))

        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False
        #przeszlo pomyslnie testy
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        return True

    def move_left(self):
        #check if can into space
        iksy = [x[0]-LEWY_LIMIT for x in self.punkty]
        if not all(iksy): return False

        #sprawdz czy nie kolajduje z innymi
        nowe_pkt=[]
        for punkt in self.punkty:
            nowe_pkt.append((punkt[0]-1, punkt[1]))

        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False
        #przeszlo pomyslnie testy
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        return True

    def move_right(self):
        #check if can into space
        iksy = [x[0]-PRAWY_LIMIT+1 for x in self.punkty]
        if not all(iksy): return False

        #sprawdz czy nie kolajduje z innymi
        nowe_pkt=[]
        for punkt in self.punkty:
            nowe_pkt.append((punkt[0]+1, punkt[1]))

        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False
        #przeszlo pomyslnie testy
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        return True

    def rysuj_punkty(self):
        temp_pts = []
        for p in self.punkty:
            temp_pts += [(p[0]*3,p[1]*3), (p[0]*3+1,p[1]*3), (p[0]*3+2,p[1]*3),
                         (p[0]*3,p[1]*3+1), (p[0]*3+1,p[1]*3+1), (p[0]*3+2,p[1]*3+1),
                         (p[0]*3,p[1]*3+2), (p[0]*3+1,p[1]*3+2), (p[0]*3+2,p[1]*3+2)]
        self.draw.point(temp_pts, fill=0)

    def zmaz_punkty(self):
        temp_pts = []
        for p in self.punkty:
            temp_pts += [(p[0]*3,p[1]*3), (p[0]*3+1,p[1]*3), (p[0]*3+2,p[1]*3),
                         (p[0]*3,p[1]*3+1), (p[0]*3+1,p[1]*3+1), (p[0]*3+2,p[1]*3+1),
                         (p[0]*3,p[1]*3+2), (p[0]*3+1,p[1]*3+2), (p[0]*3+2,p[1]*3+2)]
        self.draw.point(temp_pts, fill=255)

    def append_to_wyznaczniki(self):
        self.wyznaczniki+=(self.punkty)
        for p in self.punkty:
            self.clearing_wyznaczniki[p[1]][p[0]-LEWY_LIMIT] = 1
        

class Kwadrat(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self,draw,wyznaczniki, cw)
        self.punkty = [(5+LEWY_LIMIT,0), (6+LEWY_LIMIT,0),
                       (5+LEWY_LIMIT,1), (6+LEWY_LIMIT,1)]
        

class Z_normal(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(4+LEWY_LIMIT, 0), (5+LEWY_LIMIT, 0),
                       (5+LEWY_LIMIT, 1), (6+LEWY_LIMIT, 1)]
        self.stan = 0

    def switch_right(self):
        temp_punkty = self.punkty[:]
        p=self.punkty
        if self.stan==0:
            if p[0][1]==0: return False
            nowe_pkt = [(p[0][0]+1,p[0][1]-1), temp_punkty[1],
                        temp_punkty[0], (p[2][0]-1, p[2][1])]
        elif self.stan == 1:
            if p[0][0]==PRAWY_LIMIT-1: return False
            nowe_pkt = [temp_punkty[2], temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[3][0]+2,p[3][1])]
        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False

        #testy passed
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%2
        return True

    def switch_left(self):
        return self.switch_right()

class Z_turned(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(6+LEWY_LIMIT, 0), (5+LEWY_LIMIT, 0),
                       (5+LEWY_LIMIT, 1), (4+LEWY_LIMIT, 1)]
        self.stan = 0

    def switch_right(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 0:
            if p[0][1] == 0: return False
            nowe_pkt = [(p[1][0], p[1][1]-1), temp_punkty[1],
                        temp_punkty[0], (p[0][0], p[0][1]+1)]
        elif self.stan == 1:
            if p[0][0] == LEWY_LIMIT: return False
            nowe_pkt = [temp_punkty[2], temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[3][0]-2,p[3][1])]
        #tests passed
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%2
        return True

    def switch_left(self):
        return self.switch_right()
        

class Tau(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(4+LEWY_LIMIT,0), (5+LEWY_LIMIT,0),(6+LEWY_LIMIT,0),
                       (5+LEWY_LIMIT,1)]
        self.stan = 0

    #przekrec w prawo
    def switch_right(self):
        temp_punkty = self.punkty[:]
        #sprawdz czy mozna sie ruszyc
        p=self.punkty
        if self.stan == 0:
            if p[0][1]==0: return False
            nowe_pkt = [(p[0][0]+1,p[0][1]-1), (p[1][0],p[1][1]),
                        temp_punkty[3], temp_punkty[0]]
        elif self.stan == 1:
            if p[0][0]==PRAWY_LIMIT-1: return False
            nowe_pkt = [(p[0][0]+1,p[0][1]+1), (p[1][0],p[1][1]),
                        temp_punkty[3], temp_punkty[0]]
        elif self.stan == 2:
            if p[0][1] == DOLNY_LIMIT-1: return False
            nowe_pkt = [(p[0][0]-1,p[0][1]+1), (p[1][0],p[1][1]),
                        temp_punkty[3], temp_punkty[0]]
        else:
            if p[0][0] == LEWY_LIMIT: return False
            nowe_pkt = [(p[0][0]-1,p[0][1]-1), (p[1][0],p[1][1]),
                        temp_punkty[3], temp_punkty[0]]
        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False

        #przeszlo testy
        #wymaz stare
        self.zmaz_punkty()
        #narysuj nowe
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%4
        return True

    def switch_left(self):
        temp_punkty = self.punkty[:]
        #sprawdz czy mozna sie ruszyc
        p=self.punkty
        if self.stan == 3:
            if p[2][0]==LEWY_LIMIT: return False
            nowe_pkt = [temp_punkty[3], (p[1][0],p[1][1]),
                        (p[2][0]-1,p[2][1]+1), temp_punkty[2]]
        elif self.stan == 2:
            if p[2][1]==DOLNY_LIMIT-1: return False
            nowe_pkt = [temp_punkty[3], (p[1][0],p[1][1]),
                        (p[2][0]+1,p[2][1]+1), temp_punkty[2]]
        elif self.stan == 1:
            if p[2][0]==PRAWY_LIMIT-1: return False
            nowe_pkt = [temp_punkty[3], (p[1][0],p[1][1]),
                        (p[2][0]+1,p[2][1]-1), temp_punkty[2]]
        else:
            if p[2][1]==0: return False
            nowe_pkt = [temp_punkty[3], (p[1][0],p[1][1]),
                        (p[2][0]-1,p[2][1]-1), temp_punkty[2]]
        for punkt in nowe_pkt:
            if punkt in self.wyznaczniki: return False

        #przeszlo testy
        #wymaz stare
        self.zmaz_punkty()
        #narysuj nowe
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan-1)%4
        return True

class Kij(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(4+LEWY_LIMIT, 0), (5+LEWY_LIMIT, 0),
                       (6+LEWY_LIMIT, 0), (7+LEWY_LIMIT, 0)]
        self.stan = 0

    def switch_right(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 0:
            if p[0][1]==0 or p[0][1] == DOLNY_LIMIT-2 or p[0][1] == DOLNY_LIMIT-1: return False
            nowe_pkt = [(p[1][0],p[1][1]-1),temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[1][0],p[1][1]+2)]
        else:
            if p[0][0]==LEWY_LIMIT or p[0][0] == PRAWY_LIMIT-1 or p[0][0] == PRAWY_LIMIT-2: return False
            nowe_pkt = [(p[1][0]-1, p[1][1]), temp_punkty[1],
                        (p[1][0]+1, p[1][1]), (p[1][0]+2, p[1][1])]
        #tests passed
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%2
        return True

    def switch_left(self):
        return self.switch_right()

class L_normal(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(6+LEWY_LIMIT, 0), (5+LEWY_LIMIT, 0),
                       (4+LEWY_LIMIT, 0), (4+LEWY_LIMIT, 1)]
        self.stan = 0

    def switch_right(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 0:
            if p[0][1] == 0: return False
            nowe_pkt = [(p[1][0],p[1][1]+1), temp_punkty[1],
                        (p[1][0],p[1][1]-1), (p[2][0],p[2][1]-1)]
        elif self.stan == 1:
            if p[0][0] == PRAWY_LIMIT -1: return False
            nowe_pkt = [(p[1][0]-1,p[1][1]), temp_punkty[1],
                        (p[1][0]+1,p[1][1]), (p[2][0]+1,p[2][1])]
        elif self.stan == 2:
            if p[0][1] == DOLNY_LIMIT-1: return False
            nowe_pkt = [(p[1][0],p[1][1]-1), temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[2][0],p[2][1]+1)]
        else:
            if p[0][0] == LEWY_LIMIT: return False
            nowe_pkt = [(p[1][0]+1,p[1][1]), temp_punkty[1],
                        (p[1][0]-1,p[1][1]), (p[2][0]-1,p[2][1])]
        #testy przesly
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%4
        return True

    def switch_left(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 3:
            if p[0][0] == LEWY_LIMIT: return False
            nowe_pkt = [(p[1][0]-1,p[1][1]), temp_punkty[1],
                        (p[1][0]+1,p[1][1]), (p[0][0]+1,p[0][1])]
        elif self.stan == 2:
            if p[0][1] == DOLNY_LIMIT-1: return False
            nowe_pkt = [(p[1][0],p[1][1]+1), temp_punkty[1],
                        (p[1][0],p[1][1]-1), (p[0][0],p[0][1]-1)]
        elif self.stan == 1:
            if p[0][0] == PRAWY_LIMIT-1: return False
            nowe_pkt = [(p[0][0]+1,p[0][1]), temp_punkty[1],
                        (p[0][0]-1,p[0][1]), (p[0][0]-1, p[0][1])]
        else:
            if p[0][1] == 0: return False
            nowe_pkt = [(p[1][0],p[1][1]-1), temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[0][0],p[0][1]+1)]
        #testy git
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan-1)%4
        return True

class L_turned(Klocek):
    def __init__(self, draw, wyznaczniki, cw):
        Klocek.__init__(self, draw, wyznaczniki, cw)
        self.punkty = [(4+LEWY_LIMIT, 0), (5+LEWY_LIMIT, 0),
                       (6+LEWY_LIMIT, 0), (6+LEWY_LIMIT, 1)]
        self.stan = 0

    def switch_right(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 0:
            if p[0][1] == 0: return False
            nowe_pkt = [(p[1][0],p[1][1]-1), temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[0][0],p[0][1]+1)]
        elif self.stan == 1:
            if p[0][0] == PRAWY_LIMIT -1: return False
            nowe_pkt = [(p[1][0]+1,p[1][1]), temp_punkty[1],
                        (p[1][0]-1, p[1][1]), (p[0][0]-1,p[0][1])]
        elif self.stan == 2:
            if p[0][1] == DOLNY_LIMIT -1: return False
            nowe_pkt = [(p[1][0],p[1][1]+1), temp_punkty[1],
                        (p[1][0],p[1][1]-1), (p[0][0],p[0][1]-1)]
        else:
            if p[0][0] == 0: return False
            nowe_pkt = [(p[1][0]-1,p[1][1]), temp_punkty[1],
                        (p[1][0]+1,p[1][1]), (p[0][0]+1,p[0][1])]
        #testy passed
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan+1)%4
        return True

    def switch_left(self):
        temp_punkty = self.punkty[:]
        p = self.punkty

        if self.stan == 3:
            if p[0][0] == 0: return False
            nowe_pkt = [(p[1][0]+1,p[1][1]), temp_punkty[1],
                        (p[1][0]-1,p[1][1]), (p[2][0]-1,p[2][1])]
        elif self.stan == 2:
            if p[0][1] == DOLNY_LIMIT -1: return False
            nowe_pkt = [(p[1][0],p[1][1]-1), temp_punkty[1],
                        (p[1][0],p[1][1]+1), (p[2][0],p[2][1]+1)]
        elif self.stan == 1:
            if p[0][0] == PRAWY_LIMIT -1: return False
            nowe_pkt = [(p[1][0]-1,p[1][1]), temp_punkty[1],
                        (p[1][0]+1, p[1][1]), (p[2][0]+1,p[2][1])]
        else:
            if p[0][1]==0: return False
            nowe_pkt = [(p[1][0],p[1][1]+1), temp_punkty[1],
                        (p[1][0],p[1][1]-1), (p[2][0],p[2][1]-1)]
        #testy passed
        self.zmaz_punkty()
        self.punkty = nowe_pkt
        self.rysuj_punkty()
        self.stan = (self.stan-1)%4
        return True

        
if __name__ == '__main__':
    
    #initialize pg
    pygame.init()
    screen = pygame.display.set_mode((101,101))
    pygame.display.set_caption('.')
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([QUIT, KEYDOWN])

    #initialize display
    #20 -- D/C
    #12 -- RST
        
    DC = 20
    RST = 12
    SPI_PORT = 0
    SPI_DEVICE = 0
    disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE,
                                               max_speed_hz=4000000))
    disp.begin(contrast = 50)
    disp.clear()
    time.sleep(1)
    disp.display()

    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=0)
    draw.rectangle((LEWY_LIMIT*3-1,0,PRAWY_LIMIT*3, LCD.LCDHEIGHT-1), outline=0, fill=255)
    draw.line((LEWY_LIMIT*3,0,PRAWY_LIMIT*3-1,0),fill=255)
    draw.line((LEWY_LIMIT*3,47,PRAWY_LIMIT*3-1,47),fill=255)
    disp.image(image)
    disp.display()
    
    t = Tetris(disp, draw, image)
    
