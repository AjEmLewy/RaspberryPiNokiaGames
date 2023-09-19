from PIL import Image, ImageDraw, ImageFont

class SnakePart():
    def __init__(self, x, y, special_flag):
        self.wyznacznik = (x,y)
        self.punkty = [(x,y), (x+1,y), (x+2,y),
                       (x,y+1), (x+1,y+1), (x+2,y+2),
                       (x,y+2), (x+1,y+2), (x+2,y+2)]

class Drawer():
    def __init__(self, draw):
        self.draw = draw
        self.wyznaczniki = [] 
        self.free_party = []
        #self.punkty = []
    
    def dodaj_part(self, part):
        self.wyznaczniki.append(part.wyznacznik)
        #usun stare
        self.draw.point(part.punkty, fill=255)
        #dodaj nowe
        self.draw.point(part.punkty, fill = 0)
        #wywal z wyznacznikow
        self.wyznaczniki.remove(part.wyznacznik)

        
        
