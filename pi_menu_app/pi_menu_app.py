class ConsoleInputController(object):
	def read(self):
		return raw_input('What would you like to do? (previous / next / first / last / in / out / home)\n')

class Node(object):
	def __init__(self, label='', nodes=None, controller_fn=None, *controller_argvs):

		self.label = label
		self.parent = None
		
		if nodes is None:
			nodes = []

		self.nodes = nodes

		for node in self.nodes:
			node._set_parent(self)

		self.controller_fn = controller_fn
		self.controller_argvs = controller_argvs

	def add_node(self, node):
		self.nodes.append(node)
		node._set_parent(self)

		return self

	def _set_parent(self, node):
		self.parent = node

		return self

	def controller(self, app):
		if callable(self.controller_fn):
			return self.controller_fn(app, self, *self.controller_argvs)

		return True

class App(object):
	def __init__(self, input_adapter, node_provider, display_adapter):

		CMD_NEXT      = 'next'
		CMD_PREVIOUS  = 'previous'
		CMD_IN        = 'in'
		CMD_OUT       = 'out'
		CMD_HOME      = 'home'
		CMD_FIRST     = 'first'
		CMD_LAST      = 'last'

		self._input_adapter = input_adapter
		self._node_provider = node_provider
		self.display_adapter = display_adapter

		self._root_node = MenuNode(nodes=node_provider.nodes)
		self._highlighted_node = self._root_node.nodes[0]
		self._highlighted_index = 0;
		self._context_node = self._root_node

		self._actions = {
			self.CMD_NEXT: self._nodeNext,
			self.CMD_PREVIOUS: self._nodePrevious,
			self.CMD_IN: self._nodeIn,
			self.CMD_OUT: self._nodeOut,
			self.CMD_HOME: self._home,
			self.CMD_FIRST: self._nodeFirst,
			self.CMD_LAST: self._nodeLast
		}

	def run(self):
		try
			while(True):
				action = self._input_adapter.read()
				refresh = self._handle(action)
			
				if refresh is True:
					self._display_adapter.refresh(self._context_node, self._highlighted_node)
		except KeyboardInterrupt, SystemExit
			self._cleanup()
			raise

	def _cleanup(self):
		self.display_adapter.cleanup()

	def _handle(self, event):
		if action in self._actions 
			self._actions[action]()

	def _nodeIn(self):
		refresh = self._highlighted_node.controller(self)

		if len(self._highlighted_node.nodes) > 0:

			self._context_node = self._highlighted_node
			self._highlight_node(self._context_node.nodes[0])
			
			return True

		return refresh

	def _nodeOut(self):
		if self._context_node.parent is not None:

			self._context_node = self._context_node.parent
			self._highlight_node(self._highlighted_node.parent)

			return True

		return False

	def _nodePrevious(self):
		if(self._highlighted_index > 0):
			self._highlight_node(self._context_node.nodes[self._highlighted_index - 1])

			return True

		return False

	def _nodeFirst(self):
		if(self._highlighted_index > 0):
			self._highlight_node(self._context_node.nodes[0])

			return True
		
		return False

	def _nodeNext(self):
		if(self._highlighted_index < len(self._context_node.nodes) - 1):
			self._highlight_node(self._context_node.nodes[self._highlighted_index + 1])

			return True
		
		return False

	def _nodeLast(self):
		if(self._highlighted_index < len(self._context_node.nodes) - 1):
			self._highlight_node(self._context_node.nodes[len(self._context_node.nodes) - 1])

			return True
		
		return False

	def _home(self):

		if self._context_node is not self._root_node:
			self._context_node = self._root_node
			self._highlight_node(self._context_node.nodes[0])

			return True
	
		return False

class HD44780LcdAdapter(object):
	def __init__(self, autoscroll=True, driver=None, *driver_opts):
		if driver is None
			self.driver = Adafruit_CharLCD(*driver_opts)
		else:
			self.driver = driver

		self._autoscroll = autoscroll
		self._lines = driver.lines
		self._cols = driver.cols


	def refresh(self, context_node, highlighted_node):
		self._clear()
		node_count = 0

		for node in context_node.nodes:
			self._print_node(node, node_count, node is highlighted_node)

	def _print_node(node, line, highlight):
		self.driver.set_cursor(1, line)

		if highlight is True:
			self.driver.set_cursor(0, line)
			self.driver.write8(ord('\x3E'))

		for char in node.label[:(self._cols - 1)]:
			self.driver.write8(ord(char), True)


	def _clear(self):
		self.driver.clear()

	def cleanup(self):
		self._clear()
		
		self.driver.set_backlight(False)
		self.driver.enable_display(False)









