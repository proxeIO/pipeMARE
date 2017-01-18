import bpy
from math import pi
from mathutils import Vector
from random import seed
from random import randint as random_integer
from random import uniform as random_float


class generate:


	def __init__(self, operator, context):

		seed(operator.seed)

		self.pipes(operator, context)


	@staticmethod
	def pipe_depth(pipe, depth):

		depth = depth * 0.5

		pipe.location.y = random_float(-depth, depth)


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
			pipe_data.bevel_depth = random_float(operator.min*0.5, operator.max*0.5)
			pipe_data.bevel_resolution = operator.surface

			pipe_object.rotation_euler.x = pi*0.5

			spline = pipe_data.splines.new('POLY')

			is_straight_pipe = random_integer(1, 100) < operator.straight

			if is_straight_pipe:

				self.pipe_depth(pipe_object, operator.depth)

				self.straight_pipe(spline, operator.height, operator.width)

			else:

				self.pipe_depth(pipe_object, operator.depth)

				self.bent_pipe(operator, context, pipe_object, spline)


	def straight_pipe(self, spline, height, width):

		width = width * 0.5

		base = spline.points[-1]
		base.co.x = random_float(-width, width)

		spline.points.add(count=1)

		spline.points[-1].co.x = base.co.x
		spline.points[-1].co.y = height


	def bent_pipe(self, operator, context, pipe, spline):

		width = operator.width * 0.5

		base = spline.points[-1]
		base.co.x = random_float(-width, width)

		last_y = 0.0
		last_x = base.co.x

		while last_y < operator.height:

			spline.points.add(count=1)

			point = spline.points[-1]

			point.co.x = last_x

			point.co.y = last_y + random_float(operator.length_y*0.1, operator.length_y)

			last_y = point.co.y

			spline.points.add(count=1)

			point = spline.points[-1]

			point.co.x = last_x + random_float(-operator.length_x, operator.length_y)
			point.co.y = last_y

			if point.co.x > operator.width * 0.5:

				point.co.x -= point.co.x - operator.width * 0.5

			if point.co.x < -operator.width * 0.5:

				point.co.x -= point.co.x + operator.width * 0.5

			last_x = point.co.x

		else:

			spline.points[-1].co.y = operator.height
			spline.points[-1].co.x = last_x

			if spline.points[-2].co.y > operator.height:

				spline.points[-1].select = True
				spline.points[-2].co.y = operator.height

				try: old_active_object = bpy.data.objects[context.active_object.name]
				except: pass

				context.scene.objects.active = pipe

				bpy.ops.object.mode_set(mode='EDIT')
				bpy.ops.curve.delete(type='VERT')
				bpy.ops.object.mode_set(mode='OBJECT')

				try: context.scene.objects.active = old_active_object
				except: pass


	def decorations(self, operator, context):

		pass


	def rails(self, operator, context):

		pass
