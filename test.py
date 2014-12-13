from __future__ import print_function
from simple_menu import MenuBranch
from simple_menu import MenuLeaf
from simple_menu import MenuDisplay

branch = MenuBranch('branch icon', 'This is a branch')
leaf = MenuLeaf('leaf icon', 'This is a leaf', lambda: print("This is my payback"))

branch.nodes.append(MenuBranch('branch icon', 'This is another branch'))

for node in branch.nodes:
	print(node.label)

display = MenuDisplay([branch])
display.display()

