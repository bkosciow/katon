"""Widget for Node One sensor. Displas data from it in form of tile"""
from view.widget import Widget
from PIL import Image


class NodeOneWidget(Widget):
    """Class NodeOneWidget"""
    def __init__(self, font):
        self.font = font
        self.colours = {
            'background': (255, 250, 0),
            'digit_background': (0, 0, 0),
            'border': (244, 244, 244)
        }
        self.temperature = {
            'current': 0,
            'previous': None
        }
        self.humidity = {
            'current': 0,
            'previous': None
        }
        self.movement = {
            'current': False,
            'previous': None
        }
        self.light = {
            'current': False,
            'previous': None
        }
        self.icon = {
            'movement': Image.open('assets/image/movement.png'),
            'light': Image.open('assets/image/lightbulb.png'),
            'temperature': Image.open('assets/image/thermometer.png'),
            'humidity': Image.open('assets/image/humidity.png')
        }
        self.initialized = False

    def draw_widget(self, lcd, coords):
        """draw a tile"""
        pos_x, pos_y = coords[0]
        lcd.background_color = self.colours['background']
        lcd.fill_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        lcd.background_color = self.colours['digit_background']
        lcd.fill_rect(pos_x+35, pos_y+5, pos_x+57, pos_y+46)
        lcd.fill_rect(pos_x+62, pos_y+5, pos_x+84, pos_y+46)
        lcd.fill_rect(pos_x+35, pos_y+55, pos_x+57, pos_y+95)
        lcd.fill_rect(pos_x+62, pos_y+55, pos_x+84, pos_y+95)

        lcd.transparency_color = (0, 0, 0)
        lcd.draw_image(pos_x + 91, pos_y + 10, self.icon['temperature'])
        lcd.draw_image(pos_x + 88, pos_y + 58, self.icon['humidity'])

        lcd.color = self.colours['border']
        lcd.draw_rect(pos_x, pos_y, pos_x + 105, pos_y + 105)

        self.draw_values(lcd, coords, True)
        self.initialized = True

    def draw_values(self, lcd, coords, force=False):
        """draw values"""
        pos_x, pos_y = coords[0]
        lcd.transparency_color = self.font.get_transparency()
        current = str(self.temperature['current']).rjust(2, '0')
        previous = None if self.temperature['previous'] is None \
            else str(self.temperature['previous']).rjust(2, '0')
        if force or current != previous:
            self.draw_number(
                lcd, pos_x + 35, pos_y + 5, self.font, current, previous, 27
            )

        current = str(self.humidity['current']).rjust(2, '0')
        previous = None if self.humidity['previous'] is None \
            else str(self.humidity['previous']).rjust(2, '0')
        if force or current != previous:
            self.draw_number(
                lcd, pos_x + 35, pos_y + 55, self.font, current, previous, 27
            )

        if force or self.light['current'] != self.light['previous']:
            if self.light['current']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x + 7, pos_y + 5, self.icon['light'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x+7, pos_y+5, pos_x+27, pos_y+25)

        if force or self.movement['current'] != self.movement['previous']:
            if self.movement['current']:
                lcd.transparency_color = (0, 0, 0)
                lcd.draw_image(pos_x + 7, pos_y + 30, self.icon['movement'])
            else:
                lcd.background_color = self.colours['background']
                lcd.fill_rect(pos_x+7, pos_y+30, pos_x+27, pos_y+50)

    def change_values(self, values):
        """change values"""
        if not self.initialized:
            return
        if 'temp' in values:
            self.temperature['previous'] = self.temperature['current']
            self.temperature['current'] = values['temp']

        if 'humi' in values:
            self.humidity['previous'] = self.humidity['current']
            self.humidity['current'] = values['humi']

        if 'pir' in values:
            self.movement['previous'] = self.movement['current']
            self.movement['current'] = values['pir']

        if 'light' in values:
            self.light['previous'] = self.light['current']
            self.light['current'] = values['light']
