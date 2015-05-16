import Adafruit_CharLCD as LCD
import time
import threading

class MenuNode(object):
	def __init__(self, label='', nodes=None, controllerFn=None, *controllerArgvs):

		self.label = label
		self.parent = None
		
		if nodes is None:
			nodes = []

		self.nodes = nodes

		for node in self.nodes:
			node._set_parent(self)

		self.controllerFn = controllerFn
		self.controllerArgvs = controllerArgvs

	def add_node(self, node):
		self.nodes.append(node)
		node._set_parent(self)

		return self

	def _set_parent(self, node):
		self.parent = node

		return self

	def run(self, container):
		if callable(self.controllerFn):
			self.controllerFn(container, *self.controllerArgvs)

class MenuRouter(object):
	def __init__(self, nodes, container):	
		if nodes is None:
			nodes = []

		self._root_node = MenuNode(nodes=nodes)
		self._highlighted_node = self._root_node.nodes[0]
		self._highlighted_index = 0;
		self._context_node = self._root_node
		self._scroller = None

	def _highlight_node(self, node):
		self._highlighted_node = node
		self._highlighted_index = self._context_node.nodes.index(node)

	def nodeIn(self):
		self._highlighted_node.run(container)

		if len(self._highlighted_node.nodes) > 0:

			self._context_node = self._highlighted_node
			self._highlight_node(self._context_node.nodes[0])
		
		container.get('renderer')->render()

	def nodeOut(self):
		if self._context_node.parent is not None:

			self._context_node = self._context_node.parent
			self._highlight_node(self._highlighted_node.parent)
			container.get('renderer')->render()
		else:
			container.get('renderer')->blink()

	def nodePrevious(self):
		if(self._highlighted_index > 0):
			self._highlight_node(self._context_node.nodes[self._highlighted_index - 1])
			container.get('renderer')->render()
		else:
			container.get('renderer')->blink()

	def nodeFirst(self):
		if(self._highlighted_index > 0):
			self._highlight_node(self._context_node.nodes[0])
			container.get('renderer')->render()
		else:
			container.get('renderer')->blink()

	def nodeNext(self):
		if(self._highlighted_index < len(self._context_node.nodes) - 1):
			self._highlight_node(self._context_node.nodes[self._highlighted_index + 1])
			container.get('renderer')->render()
		else:
			container.get('renderer')->blink()

	def nodeLast(self):
		if(self._highlighted_index < len(self._context_node.nodes) - 1):
			self._highlight_node(self._context_node.nodes[len(self._context_node.nodes) - 1])
			container.get('renderer')->render()
		else:
			container.get('renderer')->blink()

	def home(self):

		self._context_node = self._root_node
		self._highlight_node(self._context_node.nodes[0])
		container.get('renderer')->render()


class MenuDisplayScroller(threading.Thread):
	def __init__(self, lcd, nodes):
		threading.Thread.__init__(self)
		self.lcd = lcd
		self.nodes = nodes
		self.stop = threading.Event()

	def join(self):
		self.stop.set()
		super(MenuDisplayScroller, self).join()

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
			
			time.sleep(0.1)


class AdafruitLCDPlateDisplayHandler(object):
	def __init__(self, menu_display):
		self._menu_display = menu_display
		self._lcd = menu_display.lcd 

	def handle(self):
		self._menu_display.home()

		while True:
			try:
				if self._lcd.is_pressed(LCD.DOWN):

					self._menu_display.nodeNext()
				
				if self._lcd.is_pressed(LCD.UP):

					self._menu_display.nodePrevious()

				if self._lcd.is_pressed(LCD.RIGHT):

					self._menu_display.nodeIn()

				if self._lcd.is_pressed(LCD.LEFT):

					self._menu_display.nodeOut()
				
				if self._lcd.is_pressed(LCD.SELECT):

					self._menu_display.home()

				time.sleep(0.1)
			
			except KeyboardInterrupt, SystemExit:
				self._menu_display.shutdown()
				raise


class ConsoleDisplayHandler(object):
	def __init__(self, menu_display):
		self._menu_display = menu_display

	def handle(self):
		self._menu_display.home()

		while True:
			try:

				action = raw_input('What would you like to do? (previous / next / first / last / in / out / home)\n')

				if action == 'next':
					self._menu_display.nodeNext()
				elif action == 'previous':
					self._menu_display.nodePrevious()
				elif action == 'in':
					self._menu_display.nodeIn()
				elif action == 'out':
					self._menu_display.nodeOut()
				elif action == 'home':
					self._menu_display.home()
				elif action == 'first':
					self._menu_display.nodeFirst()
				elif action == 'last':
					self._menu_display.nodeLast()
				else:
					print('Unknown action\n')

				time.sleep(0.1)
			
			except KeyboardInterrupt, SystemExit:
				self._menu_display.shutdown()
				raise
