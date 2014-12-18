import Adafruit_CharLCD as LCD
import time
import threading

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

class CharMenuDisplay(object):

	def __init__(self, adafruit_char_lcd_plate, nodes):
		if nodes is None:
			nodes = []

		self.root_node = MenuNode(nodes=nodes)
		self.highlighted_node = self.root_node.nodes[0]
		self.highlighted_index = 0;
		self.context_node = self.root_node
		self.scroller = None

		self.lcd = adafruit_char_lcd_plate
		self.lcd.create_char(1, [0,8,12,14,12,8,0,0])

	def display(self):

		self._draw()

		while True:
			try:
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

					self.context_node = self.root_node
					self._highlight_node(self.context_node.nodes[0])
					self._draw()

				time.sleep(0.1)
			
			except KeyboardInterrupt, SystemExit:
				if self.scroller is not None:
					self.scroller.join()

				self.lcd.enable_display(False)
				self.lcd.set_backlight(False)
				raise

	def _blink(self):
		self.lcd.set_backlight(False)
		time.sleep(0.1)
		self.lcd.set_backlight(True)

	def _draw(self):

		if(self.scroller is not None):
			self.scroller.join()

		self.lcd.clear()


		nodes_to_scroll = [self.highlighted_node]
		self._draw_node(self.highlighted_node, 0)

		if self.highlighted_index < (len(self.context_node.nodes) -1):
			nodes_to_scroll.append(self.context_node.nodes[self.highlighted_index + 1])
			self._draw_node(self.context_node.nodes[self.highlighted_index + 1], 1)

		self.scroller = DisplayScroller(self.lcd, nodes_to_scroll)
		self.scroller.daemon = True
		self.scroller.start()

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


class DisplayScroller(threading.Thread):
	def __init__(self, lcd, nodes):
		threading.Thread.__init__(self)
		self.lcd = lcd
		self.nodes = nodes
		self.stop = threading.Event()

	def join(self):
		self.stop.set()
		super(DisplayScroller, self).join()

	def run(self):
		time.sleep(0.5)

		nodeOffsets = []
		for node in self.nodes:

			nodeOffsets.append(0)

		while(not self.stop.isSet()):

			for node in self.nodes:

				nodeIndex = self.nodes.index(node)
				labelSlice = node.label[nodeOffsets[nodeIndex]:][:15]
				self.lcd.set_cursor(1, nodeIndex)
				
				for char in labelSlice:

					self.lcd.write8(ord(char), True)

				if len(node.label) > 15:

					self.lcd.set_cursor(len(labelSlice) + 1, nodeIndex)

					for space in range(15 - (len(labelSlice) -1)):

						self.lcd.write8(ord(' '), True)

				nodeOffsets[nodeIndex] += 1

				if len(node.label[nodeOffsets[nodeIndex]:][:15]) < 15:

					nodeOffsets[nodeIndex] = 0
			
			time.sleep(0.3)







