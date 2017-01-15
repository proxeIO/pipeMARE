import bpy
import random


class generate:


	def __init__(self, operator, context):

		self.amount = operator.amount
		self.width = operator.width
		self.height = operator.height
		self.depth = operator.depth
		self.length_x = operator.length_x
		self.length_y = operator.length_y
		self.min = operator.min
		self.max = operator.max
		self.straight = operator.straight
		self.decoration = operator.decoration
		self.rail = operator.rail
		self.split = operator.split
		self.bevel = operator.bevel
		self.preview = operator.preview
		self.show_bounds = operator.show_bounds
		self.show_pipes = operator.show_pipes
		self.show_decorations = operator.show_decorations
		self.show_rails = operator.show_rails


	def pipes(self, context, bounds_display=False, calc_pipes=True):

		pass


	def decorations(self, context):

		pass


	def rails(self, context):

		pass
