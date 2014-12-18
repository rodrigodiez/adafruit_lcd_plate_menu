import Adafruit_CharLCD as LCD

import random, string

from adafruit_lcd_plate_menu import MenuNode
from adafruit_lcd_plate_menu import CharMenuDisplay

#  Instantiate and configure Adafruit's Char LCD Plate lib
adafruit_char_lcd_plate = LCD.Adafruit_CharLCDPlate()
adafruit_char_lcd_plate.set_color(0.0, 0.0, 1.0)
adafruit_char_lcd_plate.set_backlight(True)

#  Here we create ten menu nodes, each of them with ten childs
#  each of them, again, with ten sub-menus
menu_nodes = []

label = 'ABCDEFGHIJKLMNOPQRSTU'
menu = MenuNode(label)
menu_nodes.append(menu)
		
label = 'ABCDEFGHIJKLMNOPQ'
menu = MenuNode(label)
menu_nodes.append(menu)

#  This is our menu display
CharMenuDisplay(adafruit_char_lcd_plate, menu_nodes).display()
