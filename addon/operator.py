import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, FloatVectorProperty, FloatProperty

from . import interface
from .config import defaults as default
from .utils import generate, update, exit


class pipe_nightmare(Operator):
	bl_idname = 'object.pipe_nightmare'
	bl_label = 'Add Pipes'
	bl_description = 'Generate random pipes.'
	bl_options = {'PRESET', 'REGISTER', 'UNDO'}


	amount = IntProperty(
		name = 'Amount',
		description = 'Maximum number of pipes',
		min = 0,
		max = 1000,
		update = update,
		default = default['amount']
	)

	width = FloatProperty(
		name = 'Width',
		description = 'Width of the area that the pipes occupy.',
		subtype = 'DISTANCE',
		min = 0,
		soft_max = 10,
		update = update,
		default = default['width']
	)

	height = FloatProperty(
		name = 'Height',
		description = 'Height of the area that the pipes occupy',
		subtype = 'DISTANCE',
		min = 0,
		soft_max = 10,
		update = update,
		default = default['height']
	)

	depth = FloatProperty(
		name = 'Depth',
		description = 'Depth of the area that the pipes occupy',
		subtype = 'DISTANCE',
		min = 0,
		soft_max = 10,
		update = update,
		default = default['depth']
	)

	length_x = FloatProperty(
		name = 'X',
		description = 'Maximum length of horizantal pipes.',
		subtype = 'DISTANCE',
		min = 0,
		soft_max = 10,
		update = update,
		default = default['length_x']
	)

	length_y = FloatProperty(
		name = 'Y',
		description = 'Maximum length of vertical pipes.',
		subtype = 'DISTANCE',
		min = 0,
		soft_max = 10,
		update = update,
		default = default['length_y']
	)

	min = FloatProperty(
		name = 'Minimum',
		description = 'The minimum thickness of the pipes.',
		subtype = 'DISTANCE',
		min = 0.0,
		max = 5.0,
		update = update,
		default = default['min']
	)

	max = FloatProperty(
		name = 'Maximum',
		description = 'The maximum thickness of the pipes.',
		subtype = 'DISTANCE',
		min = 0.0,
		max = 5.0,
		update = update,
		default = default['max']
	)

	straight = IntProperty(
		name = 'Straight Pipes',
		description = 'The amount of pipes that are straight',
		subtype = 'PERCENTAGE',
		min = 0,
		max = 100,
		update = update,
		default = default['straight']
	)

	decoration = IntProperty(
		name = 'Decorations',
		description = 'Amount of pipes that have additional decorations located along them.',
		subtype = 'PERCENTAGE',
		min = 0,
		max = 100,
		update = update,
		default = default['decoration']
	)

	rail = IntProperty(
		name = 'Rails',
		description = 'Amount of pipes that will have additional rails alongside them.',
		subtype = 'PERCENTAGE',
		min = 0,
		max = 100,
		update = update,
		default = default['rail']
	)

	split = IntProperty(
		name = 'Split',
		description = 'Amount of pipes that should be split up into smaller pipes that occupy the same path.',
		subtype = 'PERCENTAGE',
		min = 0,
		max = 100,
		update = update,
		default = default['split']
	)

	bevel = IntProperty(
		name = 'Bevel',
		description = 'Amount of pipes that should have rounded corners.',
		subtype = 'PERCENTAGE',
		min = 0,
		max = 100,
		update = update,
		default = default['bevel']
	)

	preview = BoolProperty(
		name = 'Preview',
		description = 'Preview changes in the 3D View',
		update = update,
		default = default['preview']
	)

	bounds = BoolProperty(
		name = 'Bounds',
		description = 'Display the bounds of the generated pipes in the 3D View',
		update = update,
		default = default['bounds']
	)

	pipes = BoolProperty(
		name = 'Pipes',
		description = 'Display the generated pipes in the 3D View',
		update = update,
		default = default['pipes']
	)

	decorations = BoolProperty(
		name = 'Decorations',
		description = 'Display the generated pipe decorations in the 3D View',
		update = update,
		default = default['decorations']
	)

	rails = BoolProperty(
		name = 'Rails',
		description = 'Display the generated pipe rails in the 3D View',
		update = update,
		default = default['rails']
	)


	def check(self, context):

		return True


	def draw(self, context):

		interface.draw(self, context)


	def execute(self, context):

		generate(self, context)

		return {'FINISHED'}


	def invoke(self, context, event):

		if event.type == 'ESC':

			exit()

			return {'CANCELLED'}

		return context.window_manager.invoke_props_dialog(self, width=250)
