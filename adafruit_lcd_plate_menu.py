import Adafruit_CharLCD as LCD
import time

class MenuNode(object):
	def __init__(self, label='', nodes=None, payloadFn=None, *payloadArgvs):

		self.label = label
		self.parent = None
		
		if nodes is None:
			nodes = []

		self.nodes = nodes

		for node in self.nodes:
			node._set_parent(self)

		self.payloadFn = payloadFn
		self.payloadArgvs = payloadArgvs

	def add_node(self, node):
		self.nodes.append(node)
		node._set_parent(self)

		return self

	def _set_parent(self, node):
		self.parent = node

		return self

	def payload(self, display):
		if callable(self.payloadFn):
			self.payloadFn(display, self, *self.payloadArgvs)

class MenuDisplay(object):

	def __init__(self, root_node):
		self.highlighted_node = root_node.nodes[0]
		self.highlighted_index = 0;
		self.context_node = root_node
		self.root = root_node

		self.lcd = LCD.Adafruit_CharLCDPlate()
		self.lcd.autoscroll(False)
		self.lcd.create_char(1, [0,8,12,14,12,8,0,0])
		self.lcd.create_char(2, [0,10,17,21,17,10,0,0])

		self.lcd.set_color(1.0, 1.0, 1.0)

	def display(self):

		self._draw()

		while True:
			
			if self.lcd.is_pressed(LCD.DOWN):

				if(self.highlighted_index < len(self.context_node.nodes) - 1):
					self._highlight_node(self.context_node.nodes[self.highlighted_index + 1])
					self._draw()
				else:
					self._blink()	
			
			if self.lcd.is_pressed(LCD.UP):

				if(self.highlighted_index > 0):
					self._highlight_node(self.context_node.nodes[self.highlighted_index - 1])
					self._draw()
				else:
					self._blink()

			if self.lcd.is_pressed(LCD.RIGHT):

				self.highlighted_node.payload(self)

				if len(self.highlighted_node.nodes) > 0:

					self.context_node = self.highlighted_node
					self._highlight_node(self.context_node.nodes[0])
					self._draw()

			if self.lcd.is_pressed(LCD.LEFT):

				if self.context_node.parent is not None:

					self.context_node = self.context_node.parent
					self._highlight_node(self.highlighted_node.parent)
					self._draw()
			
			if self.lcd.is_pressed(LCD.SELECT):

				self.context_node = self.root
				self._highlight_node(self.root.nodes[0])
				self._draw()

			time.sleep(0.1)

	def _blink(self):
		self.lcd.set_backlight(False)
		time.sleep(0.1)
		self.lcd.set_backlight(True)

	def _draw(self):
		self.lcd.clear()
		
		self._draw_node(self.highlighted_node, 0)

		if self.highlighted_index < (len(self.context_node.nodes) -1):
			self._draw_node(self.context_node.nodes[self.highlighted_index + 1], 1)

	def _highlight_node(self, node):
		self.highlighted_node = node
		self.highlighted_index = self.context_node.nodes.index(node)

	def _draw_node(self, node, line):
		self.lcd.set_cursor(1, line)

		if node is self.highlighted_node:
			self.lcd.set_cursor(0, line)

			icon = '\x01'

			self.lcd.write8(ord(icon), True)

		for char in node.label[:15]:
			self.lcd.write8(ord(char), True)




