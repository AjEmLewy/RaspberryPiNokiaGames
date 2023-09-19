import time, pygame, sys, threading, random, json
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont
import Adafruit_Nokia_LCD as LCD

class TwoZeroFourEight():
    def __init__(self,display, draw, image):
        self.display = display
        self.draw = draw
        self.image = image
        self.set_beggining_cond()
        self.odpal()
        

    def __str__(self):
        napis = [str(a) for a in self.pola]
        return '\n'.join([' '.join(napis[4*i:4*i+4]) for i in range(4)])


    def set_beggining_cond(self):
        self.score = 0
        self.pola = ['' for x in range(16)]
        self.mapa = {2:10, 4:10, 8:10, 16:8, 32:8, 64:8, 128:5, 256:5, 512:5, 1024:2}
        self.koniec = False
        self.add_somewhere()
        self.add_somewhere()

    def add_somewhere(self):
        free_spaces = [x for x in range(16) if self.pola[x]=='']
        
        poz = free_spaces[random.randint(0,len(free_spaces)-1)]
        val = 2 if random.randint(1,10)<10 else 4
        self.pola[poz]=val

    def move_right(self):
        prev = self.pola[:]
        temp_pola = [self.pola[0:4], self.pola[4:8], self.pola[8:12],
                     self.pola[12:16]]
        (self.pola, score) = move(temp_pola)
        self.score+=score
        if prev != self.pola: self.add_somewhere()
        
    def move_left(self):
        prev = self.pola[:]
        temp_pola = [self.pola[15:11:-1], self.pola[11:7:-1],
                     self.pola[7:3:-1],self.pola[3::-1]]
        (temp_pola, score) = move(temp_pola)
        self.pola = temp_pola[::-1]
        self.score+=score
        if prev != self.pola: self.add_somewhere()

    def move_up(self):
        prev = self.pola[:]
        temp_pola = self.pola[::-1]
        temp_pola=[temp_pola[0:16:4], temp_pola[1:16:4],
                   temp_pola[2:16:4], temp_pola[3:16:4]]
        (temp_pola, score) = move(temp_pola)
        self.pola = (temp_pola[0:16:4]+temp_pola[1:16:4]+temp_pola[2:16:4]+temp_pola[3:16:4])[::-1]
        self.score+=score;
        if prev != self.pola: self.add_somewhere()

    def move_down(self):
        prev = self.pola[:]
        temp_pola=[self.pola[0:16:4], self.pola[1:16:4],
                   self.pola[2:16:4], self.pola[3:16:4]]
        (temp_pola, score) = move(temp_pola)
        self.pola = temp_pola[0:16:4]+temp_pola[1:16:4]+temp_pola[2:16:4]+temp_pola[3:16:4]
        self.score+=score;
        if prev != self.pola: self.add_somewhere()

    def odpal(self):
        while True:
            opcja = self.draw_main_menu()
            if opcja == 0:
                self.start_game()
            elif opcja == 1:
                self.show_highscores()
            else:
                pygame.quit()
                sys.exit()
            

    def draw_main_menu(self):
        # clear first
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                            outline=0, fill=255)
        font = ImageFont.truetype("data-latin.ttf", size=12)
        self.draw.text((25,17),'START', font=font)
        self.display.image(self.image)
        self.display.display()
        option = 0
        #TODO: ustal lepsze opcje ziom
        opcje = [("START",(25,17)),
                 ("H-SCORE", (16,17)),
                 ("BACK", (27,17))]
        pygame.event.clear()
        while not self.koniec:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_RIGHT: option=(option+1)%3
                    elif event.key == pygame.K_LEFT: option = (option-1)%3
                    elif event.key == pygame.K_RETURN: return option

                    #TODO: UPIEKSZ MENU! BO SUCHE
                    self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                                        outline=0, fill=255)
                    self.draw.text(opcje[option][1],opcje[option][0], font=font)

                    #TODO strzalki
                    
                    self.display.image(self.image)
                    self.display.display()
            time.sleep(0.2)
        check_if_highscore()

    def show_highscores(self):
        with open('highscores.json') as file:
            data = json.load(file)
        hs = data['2048']
        # clear first
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                            outline=0, fill=255)
        font = ImageFont.truetype("data-latin.ttf", size=12)
        self.draw.text((20,4), "HIGHEST", font=font)
        self.draw.text((25,17), "SCORE", font=font)
        font = ImageFont.truetype("data-latin.ttf", size=15)
        #zmien styl wyswietlania wyniku
        self.draw.text((35,30), hs, font=font)
        self.display.image(self.image)
        self.display.display()
        time.sleep(3)

    def start_game(self):
        #jak zawsze wyczysc najpierw :v
        self.draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1),
                            outline=0, fill=255)
        self.draw.rectangle((0,LCD.LCDHEIGHT-2,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=0)
        self.draw.line((1,1,83,1),fill=0)
        self.draw.line((1,1,1,LCD.LCDWIDTH-1),fill=0)
        self.draw.rectangle((82,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=0)
        self.draw_tiles()

        #main loop
        pygame.event.clear()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.move_down()
                    elif event.key == pygame.K_RIGHT:
                        self.move_right()
                    elif event.key == pygame.K_LEFT:
                        self.move_left()
                    self.draw_tiles()
                    #self.draw_score()
                    time.sleep(0.2)
                    pygame.event.clear()
        
                
    def draw_tiles(self):
        self.draw.rectangle((1,1,81, LCD.LCDHEIGHT-1),
                            outline=0, fill=255)
        font = ImageFont.truetype("data-latin.ttf", size=8)
        for i in range(16):
            if(self.pola[i]!=''):
                self.draw.rectangle((20*(i%4)+2, 11*int(i/4)+2, 20*(i%4)+22, 11*int(i/4)+12),
                                    outline = 0, fill=255)
                self.draw.text((20*(i%4)+self.mapa[self.pola[i]], 11*int(i/4)+2), str(self.pola[i]), font=font)
        self.display.image(self.image)
        self.display.display()

    #TODO: przemysl czy jest miejsce na score teraz.
    def draw_score(self):
        return
        #TODO: ustal gdzie ma to byc.
        draw.rectangle((62,28, 83, 46), outline=0, fill = 0)
        font = ImageFont.truetype("data-latin.ttf", size=12)
        draw.text((62,30), '{0}'.format(str(score).zfill(3)), font=font, fill=255)

    def check_if_highscore(self):
        with open('highscores.json') as file:
            data = json.load(file)
        hs = int(data['2048'])
        if self.score>hs:
            with open('highscores.json', 'w') as file:
                data['2048'] = str(self.score)
                json.dump(data,file)


def move(pola):
    score=0
    for pole in pola:
        #3 pole
        if pole[2]!='':
            if pole[3] == '':
                pole[3]=pole[2]
                pole[2]=''
            else:
                if pole[3]==pole[2]:
                    pole[3]*=2
                    score+=pole[3]
                    pole[2]=''
        #2 pole
        if pole[1]!='':
            if (pole[2]=='' and pole[3]==''):
                pole[3]=pole[1]
                pole[1]=''
            elif(pole[3]!='' and pole[2] == ''):
                if pole[3]==pole[1]:
                    pole[3]*=2
                    score+=pole[3]
                else:
                    pole[2]=pole[1]
                pole[1]=''
            elif(pole[2]!=''):
                if pole[2]==pole[1]:
                    pole[2]*=2
                    score+=pole[2]
                    pole[1]=''
            
        #1 pole
        if pole[0]!='':
            if(pole[3]=='' and pole[2] =='' and pole[1]==''):
               pole[3] = pole[0]
               pole[0] = ''
            elif (pole[3] != '' and pole[2] == '' and pole[1] == ''):
               if pole[3] == pole[0]:
                   pole[3]*=2
                   score+=pole[3]
               else:
                   pole[2]=pole[0]
               pole[0]=''
            elif (pole[2] != '' and pole[1]==''):
                if pole[2] == pole[0]:
                    pole[2]*=pole[0]
                    score+=pole[2]
                else:
                    pole[1]=pole[0]
                pole[0]=''
            elif (pole[1]!= ''):
                if( pole[1]==pole[0]):
                    pole[1]*=2
                    score+=pole[1]
                    pole[0]=''
                
    return (pola[0]+pola[1]+pola[2]+pola[3], score)


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
    draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
    disp.image(image)
    disp.display()
    
    t = TwoZeroFourEight(disp, draw, image)
