import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image, ImageDraw, ImageFont

#21 -- D/C
#20 -- RST

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

#draw smth

draw = ImageDraw.Draw(image)

draw.rectangle((0,0,LCD.LCDWIDTH-1, LCD.LCDHEIGHT-1), outline=0, fill=255)

font = ImageFont.truetype("data-latin.ttf", size=12)

draw.text((27,17),"BACK", font=font)
disp.image(image)
disp.display()
