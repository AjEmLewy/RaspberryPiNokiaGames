import time, pygame, sys, random, json
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont
#import snejk_classes

class Snejk():
    def __init__(self, display, draw, image):
        self.display = display
        self.draw = draw
        self.image = image
        self.groj_snejka()
        

    def main_menu(self):
        #option currently chosen
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                            outline=0, fill=255)
        self.display.image(self.image)
        self.display.display()
        font = ImageFont.truetype("data-latin.ttf", size=12)
        self.draw.text((20,3), 'START', font=font)
        self.draw.text((20,17), 'HSCORES', font=font)
        self.draw.text((20,31), 'QUIT', font=font)
        return self.get_option()

    def get_option(self):
        option = 0
        points =[(3, 14*option+9), (4, 14*option+9), (5, 14*option+9),
                 (6, 14*option+9), (5, 14*option+8), (5, 14*option+10)]
        self.draw.point(points, fill=0)
        self.display.image(self.image)
        self.display.display()
        while True:
            #zbierz eventy
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.draw.point(points, fill=255)
                        option = (option-1)%3
                        points =[(3, 14*option+9), (4, 14*option+9),
                                 (5, 14*option+9),(6, 14*option+9),
                                 (5, 14*option+8), (5, 14*option+10)]
                        self.draw.point(points, fill=0)
                    if event.key == pygame.K_DOWN:
                        self.draw.point(points, fill=255)
                        option = (option+1)%3
                        points =[(3, 14*option+9), (4, 14*option+9),
                                 (5, 14*option+9),(6, 14*option+9),
                                 (5, 14*option+8), (5, 14*option+10)]
                        self.draw.point(points, fill=0)
                    if event.key == pygame.K_RETURN:
                        time.sleep(1)
                        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                                            outline=0, fill=255)
                        return option
                    self.display.image(self.image)
                    self.display.display()
            # w zaleznosci od opcji wyswietl 14*options +9
            time.sleep(0.1)

    def gra(self):
        zakres = (61,46)
        score = 0
        #narysuj score
        self.draw.rectangle((0,0,zakres[0], zakres[1]), outline=0, fill=255)
        self.draw.rectangle((zakres[0]+1,0,83,47), outline = 0, fill = 0)
        self.draw.line((0,47,83,47), fill=255)
        font = ImageFont.load_default()
        self.draw.text((66,1), 'SC', font=font, fill=255)
        self.draw.text((69,9), 'O', font=font, fill=255)
        self.draw.text((66,18), 'RE', font=font, fill=255)
        self.dodaj_score(score)

        #cialo snejka
        ruch = 'right'
        facing = 'right'
        okres = 0.3
        wyznaczniki = [(10,16),(13,16),(16,16),(19,16),(22,16)]
        for wyznacznik in wyznaczniki:
            self.narysuj_punkt(wyznacznik)
        self.display.image(self.image)
        self.display.display()
        time.sleep(0.4)
        star_point_on_screen = False
        star_points = []
        pygame.event.clear()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == pygame.K_UP and facing != 'down':
                        ruch = 'up'
                    if event.key == pygame.K_DOWN and facing != 'up':
                        ruch = 'down'
                    if event.key == pygame.K_RIGHT and facing != 'left':
                        ruch = 'right'
                    if event.key == pygame.K_LEFT and facing!= 'right':
                        ruch = 'left'
            #poza eventem
            #wykonaj ruch
            head = wyznaczniki[-1]
            tail = wyznaczniki[0]
            if ruch == 'right':
                if head[0] + 3 >= zakres[0] or (head[0]+3 ,head[1]) in wyznaczniki:
                    return score
                wyznaczniki.append((head[0]+3,head[1]))
                head = wyznaczniki[-1]
                if (head[0], head[1]) in star_points:
                    star_points.remove((head[0],head[1]))
                    star_point_on_screen = False
                    score+=1
                    self.dodaj_score(score)
                    okres= 0.3*(0.95**(int(score/5)))
                    
                else:
                    self.zmaz_punkt(tail)
                    self.narysuj_punkt(head)
                    del wyznaczniki[0]
                facing = 'right'
                
            if ruch == 'left':
                if head[0] - 3 <= 0 or (head[0]-3 ,head[1]) in wyznaczniki:
                    return score
                wyznaczniki.append((head[0]-3,head[1]))
                head = wyznaczniki[-1]
                if (head[0], head[1]) in star_points:
                    star_points.remove((head[0],head[1]))
                    star_point_on_screen = False
                    score+=1
                    self.dodaj_score(score)
                    okres= 0.3*(0.95**(int(score/5)))
                else:
                    self.zmaz_punkt(tail)
                    self.narysuj_punkt(head)
                    del wyznaczniki[0]
                facing = 'left'
                
            if ruch == 'down':
                if head[1] + 3 >= zakres[1] or (head[0] ,head[1] +3) in wyznaczniki:
                    return score
                wyznaczniki.append((head[0],head[1]+3))
                head = wyznaczniki[-1]
                if (head[0], head[1]) in star_points:
                    star_points.remove((head[0],head[1]))
                    star_point_on_screen = False
                    score+=1
                    self.dodaj_score(score)
                    okres= 0.3*(0.95**(int(score/5)))
                else:
                    self.zmaz_punkt(tail)
                    self.narysuj_punkt(head)
                    del wyznaczniki[0]
                facing = 'down'

            if ruch == 'up':
                if head[1] - 3 <= 0 or (head[0] ,head[1] - 3) in wyznaczniki:
                    return score
                wyznaczniki.append((head[0],head[1] - 3))
                head = wyznaczniki[-1]
                if (head[0], head[1]) in star_points:
                    star_points.remove((head[0],head[1]))
                    star_point_on_screen = False
                    score+=1
                    self.dodaj_score(score)
                    okres= 0.3*(0.95**(int(score/5)))
                else:
                    self.zmaz_punkt(tail)
                    self.narysuj_punkt(head)
                    del wyznaczniki[0]
                facing = 'up'
                
            #dodaj gdzies na mapie jesli trzeba
            if(not star_point_on_screen):
                star_points.append(self.dodaj_wolny_punkt(wyznaczniki))
                star_point_on_screen = True
            

            self.display.image(self.image)
            self.display.display()
            time.sleep(okres)
        

    def narysuj_punkt(self, wyznacznik):
        (x,y) = wyznacznik
        self.draw.point([(x,y),(x+1,y),(x+2,y),
                    (x,y+1),(x+1,y+1),(x+2,y+1),
                    (x,y+2),(x+1,y+2),(x+2,y+2)], fill=0)

    def zmaz_punkt(self, wyznacznik):
        (x,y) = wyznacznik
        self.draw.point([(x,y),(x+1,y),(x+2,y),
                    (x,y+1),(x+1,y+1),(x+2,y+1),
                    (x,y+2),(x+1,y+2),(x+2,y+2)], fill=255)
                  
    def dodaj_wolny_punkt(self, wyznaczniki):
        while True:
            (x,y) = (random.randint(1,19)*3+1,random.randint(1,14)*3+1)
            if (x,y) not in wyznaczniki:
                self.narysuj_punkt((x,y))
                return (x,y)
    def dodaj_score(self, score):
        self.draw.rectangle((62,28, 83, 46), outline=0, fill = 0)
        font = ImageFont.truetype("data-latin.ttf", size=12)
        self.draw.text((62,30), '{0}'.format(str(score).zfill(3)), font=font, fill=255)
        
    def check_if_highscore(self,wynik):
        with open('highscores.json') as file:
            data = json.load(file)
        if wynik > int(data['snejk']):
            self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
            font = ImageFont.truetype("data-latin.ttf", size=12)
            self.draw.text((30,3), 'NEW', font=font)
            self.draw.text((12,20), 'HIGHSCORE', font=font)
            self.display.image(self.image)
            disp.display()
            time.sleep(3)
            data['snejk'] = str(wynik)
            
            with open('highscores.json', 'w') as file:
                json.dump(data,file)

    def show_highscore(self):
        with open('highscores.json') as file:
            data = json.load(file)
        hs = data['snejk']
        print(hs)
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
        font = ImageFont.truetype("data-latin.ttf", size=12)
        self.draw.text((20,4), "HIGHEST", font=font)
        self.draw.text((25,17), "SCORE", font=font)
        font = ImageFont.truetype("data-latin.ttf", size=15)
        self.draw.text((35,30), hs, font=font)
        self.display.image(self.image)
        self.display.display()
        time.sleep(3)
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
    def groj_snejka(self):
        while True:
            a = self.main_menu()
            if a==2:
                return
            elif a == 1:
                self.show_highscore()
            else:
                wynik = self.gra()
                self.check_if_highscore(wynik)
                self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
                time.sleep(2)
            
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
    time.sleep(2)
    disp.display()

    image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
    draw = ImageDraw.Draw(image)

    #draw rectangle
    draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)

    #load main menu
    '''
    while True:
        a = main_menu(draw)
        if a==2:
            pass
        elif a == 1:
            show_highscore(draw)
        else:
            wynik = gra(draw)
            check_if_highscore(wynik, draw)
            draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
            time.sleep(2)'''

