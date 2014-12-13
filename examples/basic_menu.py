from simple_menu import MenuNode
from simple_menu import MenuDisplay

import requests

#  This is our root menu node. We will build our menu structure within it
root_node = MenuNode()

#  Ten elements in the first menu level, each of them with 10 childs
for x in range(1,11):
	child = MenuNode('Menu %d' % (x))

	for y in range(1,11):
		sub_child = MenuNode('Child %d-%d' % (x, y))
		child.add_node(sub_child)

	root_node.add_node(child)
		
#  This is our menu display. It uses our previously defined menu as a data source and let us
#  operate with it
display = MenuDisplay(root_node)
display.display()

#  Enjoy trasversing!