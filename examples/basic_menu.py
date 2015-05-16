import Adafruit_CharLCD as LCD

from adafruit_lcd_plate_menu import MenuNode
from adafruit_lcd_plate_menu import MenuDisplay
from adafruit_lcd_plate_menu import AdafruitLCDPlateDisplayHandler
from adafruit_lcd_plate_menu import ConsoleDisplayHandler


#  Instantiate and configure Adafruit's Char LCD Plate lib
adafruit_char_lcd_plate = LCD.Adafruit_CharLCDPlate()
adafruit_char_lcd_plate.set_color(0.0, 0.0, 1.0)
adafruit_char_lcd_plate.set_backlight(True)

#  Here we create ten menu nodes, each of them with ten childs
#  each of them, again, with ten sub-menus
menu_nodes = []
for x in range(1,11):
	menu = MenuNode('Menu %d' % (x))

	for y in range(1,11):
		sub_menu = MenuNode('Menu %d-%d' % (x, y))

		for z in range(1,11):
			sub_sub_menu = MenuNode('Menu %d-%d-%d' % (x,y,z))
			sub_menu.add_node(sub_sub_menu)

		menu.add_node(sub_menu)

	menu_nodes.append(menu)
		
#  This is our menu display
display = MenuDisplay(menu_nodes, adafruit_char_lcd_plate)
ConsoleDisplayHandler(display).handle()
#  Enjoy trasversing the menu!