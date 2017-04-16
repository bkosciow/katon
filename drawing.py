from driver.nju6450.gpio import GPIO
from driver.nju6450.nju6450 import NJU6450
from driver.ssd1306.spi import SPI
from driver.ssd1306.ssd1306 import SSD1306
import random

def hole(o, x, y):
    o.draw_pixel(x+1, y)
    o.draw_pixel(x+2, y)
    o.draw_pixel(x+3, y)
    o.draw_pixel(x+1, y + 4)
    o.draw_pixel(x+2, y + 4)
    o.draw_pixel(x+3, y + 4)
    o.draw_pixel(x, y + 1)
    o.draw_pixel(x+4, y + 1)
    o.draw_pixel(x, y + 2)
    o.draw_pixel(x+4, y + 2)
    o.draw_pixel(x, y + 3)
    o.draw_pixel(x+4, y + 3)

def draw_points(o):
    for _ in range(0, 50):
        hole(o, random.randint(2,o.width - 10), random.randint(2,o.height-10))


lcd_oled = SSD1306(128, 64, SPI())
lcd_oled.init()
lcd_oled.auto_flush = False

lcd_nju = NJU6450(122, 32, GPIO())
lcd_nju.init()
lcd_nju.auto_flush = False

lcd_oled.draw_line(0, 0, 100, 20)
#draw_points(lcd_oled)
#draw_points(lcd_nju)

lcd_oled.flush(True)
lcd_nju.flush(True)
