import Adafruit_CharLCD as LCD

class MenuNode(object):
	def __init__(self, lead_icon, label):

		self.lead_icon = lead_icon
		self.label = label
		self.parent = None

	def set_parent(node):
		self.parent = node

		return self

class MenuBranch(MenuNode):
	def __init__(self, lead_icon, label, nodes=None):

		super(MenuBranch, self).__init__(lead_icon, label)

		if nodes is None:
			nodes = []
		
		self.nodes = nodes

	def add_node(node):
		self.nodes.append(node)
		node.set_parent(self)

		return self

class MenuLeaf(MenuNode):
	def __init__(self, lead_icon, label, payback):

		super(MenuLeaf, self).__init__(lead_icon, label)

		self.payback = payback

class MenuDisplay(object):
	def __init__(self, nodes):
		self.nodes = nodes
		self.active_node = nodes.index(0)

	def display():
		lcd = LCD.Adafruit_CharLCDPlate()
		lcd.set_color(1.0, 1.0, 1.0)
		lcd.clear()

		lcd.message('Ready!')


