import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty, FloatVectorProperty, FloatProperty

from . import interface
from .config import defaults as default
from .utils import update


class pipe_nightmare(Operator):
	bl_idname = 'object.pipe_nightmare'
	bl_label = 'Pipe Nightmare'
	bl_description = 'Generate random pipes.'
	bl_options = {'PRESET'}


	preview = BoolProperty(
		name = 'Preview',
		description = 'Preview changes in the 3D View',
		update = update(self, context),
		default = default['preview']
	)

	bounds = BoolProperty(
		name = 'Bounds',
		description = 'Display the bounds of the generated pipes in the 3D View',
		update = update(self, context),
		default = default['bounds']
	)

	pipes = BoolProperty(
		name = 'Pipes',
		description = 'Display the generated pipes in the 3D View',
		update = update(self, context),
		default = default['pipes']
	)

	amount = IntProperty(
		name = 'Amount',
		description = 'Maximum number of pipes',
		update = update(self, context),
		default = default['amount']
	)

	width = FloatVectorProperty(
		name = 'Width',
		description = 'Width of the area that the pipes occupy.',
		subtype = 'TRANSLATION',
		min = 0,
		soft_max = 10,
		update = update(self, context),
		default = default['width']
	)

	height = FloatVectorProperty(
		name = 'Height',
		description = 'Height of the area that the pipes occupy',
		subtype = 'TRANSLATION',
		min = 0,
		soft_max = 10,
		update = update(self, context),
		default = default['height']
	)

	length_x = FloatVectorProperty(
		name = 'X',
		description = 'Maximum length of horizantal pipes.',
		subtype = 'TRANSLATION',
		min = 0,
		soft_max = 10,
		update = update(self, context),
		default = default['length_x']
	)

	length_y = FloatVectorProperty(
		name = 'Y',
		description = 'Maximum length of vertical pipes.',
		subtype = 'TRANSLATION',
		min = 0,
		soft_max = 10,
		update = update(self, context),
		default = default['length_y']
	)

	straight = FloatProperty(
		name = 'Straightness',
		description = 'The amount of pipes that are straight',
		subtype = 'PERCENTAGE',
		update = update(self, context),
		default = default['straight']
	)

	decoration = FloatProperty(
		name = 'Decorations',
		description = 'Amount of pipes that have additional decorations located along them.',
		subtype = 'PERCENTAGE',
		update = update(self, context),
		default = default['decoration']
	)

	rail = FloatProperty(
		name = 'Rails',
		description = 'Amount of pipes that will have additional rails alongside them.',
		subtype = 'PERCENTAGE',
		update = update(self, context),
		default = default['rail']
	)

	split = FloatProperty(
		name = 'Split',
		description = 'Amount of pipes that should be split up into smaller pipes that occupy the same path.',
		subtype = 'PERCENTAGE',
		update = update(self, context),
		default = default['split']
	)

	bevel = FloatProperty(
		name = 'Bevel',
		description = 'Amount of pipes that should have rounded corners.',
		subtype = 'PERCENTAGE',
		update = update(self, context),
		default = default['bevel']
	)


	def check(self, context):

		return True


	def draw(self, context):

		interface.draw(self, context)


	def execute(self, context):

		return {'FINISHED'}


	def invoke(self, context, event):

		context.window_manager.invoke_props_dialog(self, width=250)
