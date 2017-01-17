import bpy
from math import pi
from mathutils import Vector
from random import seed
from random import randint as random_integer
from random import uniform as random_float


class generate:


	def __init__(self, operator, context):

		seed(operator.seed)

		if operator.create_empty and operator.hide_lines and not operator.convert:

			context.space_data.show_relationship_lines = False if operator.hide_lines else True

		self.pipes(operator, context)


	@staticmethod
	def pipe_location(pipe, width, depth, thickness):

		width = width * 0.5
		depth = depth * 0.5

		pipe.location.x = random_float(-width+thickness, width-thickness)
		pipe.location.y = random_float(-depth+thickness, depth-thickness)


	def pipes(self, operator, context):

		empty = None if not operator.create_empty and operator.convert else bpy.data.objects.new(name='Pipes', object_data=None)

		if operator.create_empty and not operator.convert:

			context.scene.objects.link(empty)
			context.scene.objects.active = empty
			empty.empty_draw_type = 'CUBE'
			empty.location.z = operator.height*0.5
			empty.scale = Vector((operator.width*0.5, operator.depth*0.5, operator.height*0.5))

		for index in range(operator.amount):

			name = 'Pipe.{}'.format(str(index+1).zfill(len(str(operator.amount))))

			pipe_data = bpy.data.curves.new(name=name, type='CURVE')
			pipe_object = bpy.data.objects.new(name=name, object_data=pipe_data)
			context.scene.objects.link(pipe_object)

			if operator.create_empty and not operator.convert:

				pipe_object.select = True
				bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
				pipe_object.select = False

			pipe_data.fill_mode = 'NONE'
			pipe_data.bevel_depth = random_float(operator.min, operator.max)
			pipe_data.bevel_resolution = operator.surface

			pipe_object.rotation_euler.x = pi*0.5

			spline = pipe_data.splines.new('POLY')

			is_straight_pipe = random_integer(1, 100) < operator.straight

			if is_straight_pipe:

				self.straight_pipe(operator, pipe_object, spline)

			else:

				pass



	def straight_pipe(self, operator, pipe, spline):

		spline.points.add(count=1)

		spline.points[1].co.y = operator.height

		self.pipe_location(pipe, operator.width, operator.depth, pipe.data.bevel_depth)


	def decorations(self, operator, context):

		pass


	def rails(self, operator, context):

		pass
