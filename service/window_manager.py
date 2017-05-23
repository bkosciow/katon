"""Window Manager"""
import threading
import time
import math
from view.widget import Clickable


class WidgetHolder(object):
    """Widget Holder"""
    def __init__(self, coords, slots, widget):
        self.coords = coords
        self.slots = slots
        self.widget = widget


class Page(object):
    """Page class"""
    def __init__(self, size):
        self.size = size
        self.widgets = {}

    def add_widget(self, name, widget_holder):
        """add widget holder to page"""
        if self.validate_slot(widget_holder.slots):
            self.widgets[name] = widget_holder
        else:
            raise AttributeError('one or more slots in use ', widget_holder.slots)

    def validate_slot(self, slots):
        """checks if given slots are empty"""
        for slot in slots:
            for widget in self.widgets:
                if slot in self.widgets[widget].slots:
                    return False

        return True

    def find_slot(self):
        pos_x, pos_y = 0, 0
        pass


class WindowManager(threading.Thread):
    """Window Manager"""
    size = {
        "widget_height": 106,
        "widget_width": 106,
        "grid_height": 0,
        "grid_width": 0,
        "margin_height": 0,
        "margin_width": 0,
    }

    def __init__(self, config):
        threading.Thread.__init__(self)
        self.active_page = 0
        self.lcd = config.lcd
        self._calculate_grid()
        self.pages = [
            Page((self.size['grid_width'], self.size['grid_height']))
        ]
        config.init_touch(self.click)
        self.work = True
        self.widgets = []
        self.draw_page = True

    def add_widget(self, name, slots, widget, page=0):
        """add widget to grid, calculate (x,y)"""
        position = []
        for coords in slots:
            if coords[0] > self.size['grid_width'] or coords[1] > self.size['grid_height']:
                raise Exception('Widget out of screen ', name, slots)
            position.append((
                coords[0]*(self.size["widget_width"] + self.size['margin_width']),
                coords[1]*(self.size["widget_height"] + self.size['margin_height'])
            ))

        if page > len(self.pages)-1:
            self._add_page(page)
        self.pages[page].add_widget(name, WidgetHolder(position, slots, widget))

    def auto_add_widget(self, name, widget):
        """find free slot and add widget"""
        pass

    def _add_page(self, page):
        """add new page"""
        if len(self.pages) < page:
            raise Exception('Cannot create page '+str(page))

        self.pages.append(
            Page((self.size['grid_width'], self.size['grid_height']))
        )

    def _find_slot_page(self):
        """find first free slot"""
        for page in self.pages:
            slot = page.find_slot()

    def run(self):
        """main loop - drawing"""
        self.widgets = self.pages[self.active_page].widgets
        while self.work:
            if self.draw_page:
                self._draw_widgets()
            for holder in self.widgets:
                self.widgets[holder].widget.draw_values(
                    self.lcd, self.widgets[holder].coords
                )
            time.sleep(0.025)

    def _draw_widgets(self):
        """draw widgets"""
        self.lcd.init()
        for holder in self.widgets:
            self.widgets[holder].widget.draw_widget(
                self.lcd, self.widgets[holder].coords
            )
        self.draw_page = False

    def stop(self):
        """stops a thread"""
        self.work = False

    def set_widget_color(self, name, key, value):
        """change colour"""
        widget = self.get_widget(name)
        if widget:
            widget.colours[key] = value

    def get_widget(self, name):
        """get widget by name"""
        for page in self.pages:
            widgets = page.widgets
            if name in widgets:
                return widgets[name].widget

        return None

    def get_widgets(self):
        """returns widgets dictionary"""
        return_widgets = {}
        for page in self.pages:
            widgets = page.widgets
            for handler in widgets:
                return_widgets[handler] = widgets[handler].widget

        return return_widgets

    def click(self, point):
        """execute click event"""
        if point is None:
            return
        if self._execute_internal_event(point):
            return
        pos_x, pos_y = point
        holders = self.pages[self.active_page].widgets
        found = (None, None)
        for name in holders:
            idx = 0
            if isinstance(holders[name].widget, Clickable):
                for coords in holders[name].coords:
                    if coords[0] < pos_x < coords[0] + self.size["widget_width"] and coords[1] < pos_y < coords[1] + self.size["widget_height"]:
                        found = (name, idx, pos_x - coords[0], pos_y - coords[1])
                        break
                    idx += 1

        if all(val is not None for val in found):
            self.pages[self.active_page].widgets[found[0]].widget.action(*found)

    def _execute_internal_event(self, point):
        """execute internal event"""
        if self.lcd.width / 2 - 45 < point[0] < self.lcd.width / 2 + 45 and 0 < point[1] < 60:
            self._page_previous()
            return True
        if self.lcd.width / 2 - 45 < point[0] < self.lcd.width / 2 + 45 and \
            self.lcd.height - 60 < point[1] < self.lcd.height:
            self._page_next()
            return True
        return False

    def _page_previous(self):
        """switch to prev page"""
        if self.active_page > 0:
            self.widgets = self.pages[self.active_page-1].widgets
            self.draw_page = True
            self.active_page -= 1

    def _page_next(self):
        """switch to next page"""
        if self.active_page < len(self.pages)-1:
            self.widgets = self.pages[self.active_page+1].widgets
            self.draw_page = True
            self.active_page += 1

    def _calculate_grid(self):
        """calculate grid size"""
        self.size['grid_width'] = (self.lcd.width-1) // self.size['widget_width']
        self.size['grid_height'] = (self.lcd.height-1) // self.size['widget_height']

        margin_width = self.lcd.width - (self.size['grid_width'] * self.size['widget_width'])
        margin_height = self.lcd.height - (self.size['grid_height'] * self.size['widget_height'])
        self.size['margin_height'] = math.floor(margin_height / (self.size['grid_height'] -1))
        self.size['margin_width'] = math.floor(margin_width / (self.size['grid_width'] - 1))
