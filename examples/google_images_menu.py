from adafruit_lcd_plate_menu import MenuNode
from adafruit_lcd_plate_menu import MenuDisplay

import requests

#  This is a payload function. When a menu node with a payload function
#  is selected, the function gets executed. This is done before rendering
#  the next menu tree, if any.
# 
#  Every payload function receives
# 
#    - menu_display: It lets you take the control of the LCD,
#      to draw, to access the underlying Adafruit library. Just return
#      when you want the main button loop to take the control back.
# 
#    - selected_node: It lets you traverse the menu and change it
#      dynamically.
# 
#    - *argvs: The *payloadFnArgvs* (if any) that you provided when creating
#      the node instance
# 
#  This payload function queries google's APIs for images matching a keyword,
#  then build a menu inside the selected_node and finally, by returning the
#  control to the menu display, that list of results is rendered.
#  
def google_menu_build(menu_display, selected_node, *argvs):
	r = requests.get('https://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=' + argvs[0])
	data = r.json()

	for result in data['responseData']['results']:
		selected_node.add_node(MenuNode(result['titleNoFormatting']))

	return

#  This is our root menu node. We will build our menu structure within it
root_node = MenuNode()

#  This node, when rendered, will display 'Raspberry images' as its title.
#  When selected, 'google_menu_build' function will be executed and
#  'raspberry' will be provided as an argument to query google
root_node.add_node(MenuNode('Raspberry images', None, google_menu_build, 'raspberry'))

#  Same as above, but using 'python' as query
root_node.add_node(MenuNode('Python images', None, google_menu_build, 'python'))

#  Same as above, but using 'london' as query
root_node.add_node(MenuNode('London images', None, google_menu_build, 'london'))

#  This is our menu display. It uses our previously defined menu as a data source and let us
#  operate with it
display = MenuDisplay(root_node)
display.display()


#  Enjoy adapting it!
