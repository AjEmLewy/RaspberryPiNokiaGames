import time, pygame, sys, threading, random, json
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont


def draw_main_menu():
    #option currently chosen
    draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)
    font = ImageFont.truetype("data-latin.ttf", size=12)
    draw.text((19,3), 'SNAKE', font=font)
    draw.text((20,17), '2048', font=font)
    draw.text((20,31), 'QUIT', font=font)
    return get_option()
    

def get_option():
    option = 0
    points =[(3, 14*option+9), (4, 14*option+9), (5, 14*option+9),
             (6, 14*option+9), (5, 14*option+8), (5, 14*option+10)]
    draw.point(points, fill=0)
    disp.image(image)
    disp.display()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_UP:
                    draw.point(points, fill=255)
                    option = (option-1)%3
                    points =[(3, 14*option+9), (4, 14*option+9),
                             (5, 14*option+9),(6, 14*option+9),
                             (5, 14*option+8), (5, 14*option+10)]
                    draw.point(points, fill=0)
                    disp.image(image)
                    disp.display()
                if event.key == pygame.K_DOWN:
                    draw.point(points, fill=255)
                    option = (option+1)%3
                    points =[(3, 14*option+9), (4, 14*option+9),
                             (5, 14*option+9),(6, 14*option+9),
                             (5, 14*option+8), (5, 14*option+10)]
                    draw.point(points, fill=0)
                    disp.image(image)
                    disp.display()
                if event.key == pygame.K_RETURN:
                    return option
        # w zaleznosci od opcji wyswietl 14*options +9
        time.sleep(0.2)


def start():
    while True:     
        opcja = draw_main_menu()
        if opcja == 0:
            import snejk
            #zamien snejka na klase
            snejk.Snejk(disp,draw,image)
        elif opcja == 1:
            import true2048
            t = true2048.TwoZeroFourEight(disp, draw, image)
        else:
            pygame.quit()
            sys.exit()
        
        
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
start()
