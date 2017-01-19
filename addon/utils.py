import bpy
from math import pi
from mathutils import Vector
from random import seed
from random import randint as random_integer
from random import uniform as random_float


class generate:


	class pipe:


		class bent:


			def __init__(self, operator, context, pipe, spline):

				width = operator.width * 0.5

				base = spline.points[-1]
				base.co.x = random_float(-width, width)

				last_y = 0.0
				last_x = base.co.x

				while last_y < operator.height:

					spline.points.add(count=2)

					point1 = spline.points[-2]
					point2 = spline.points[-1]

					point1.co.x = last_x
					point1.co.y = last_y + random_float(operator.length_y*0.1, operator.length_y)

					last_y = point1.co.y

					point2.co.x = last_x + random_float(-operator.length_x, operator.length_y)
					point2.co.y = last_y

					if point2.co.x > operator.width * 0.5:

						point2.co.x -= point2.co.x - operator.width * 0.5

					if point2.co.x < -operator.width * 0.5:

						point2.co.x -= point2.co.x + operator.width * 0.5

					last_x = point2.co.x

				else:

					spline.points[-1].co.y = operator.height
					spline.points[-1].co.x = last_x

					if spline.points[-2].co.y > operator.height:

						spline.points[-1].select = True
						spline.points[-2].co.y = operator.height


						old_active_object = bpy.data.objects[context.active_object.name] if context.active_object else None

						context.scene.objects.active = pipe

						bpy.ops.object.mode_set(mode='EDIT')
						bpy.ops.curve.delete(type='VERT')
						bpy.ops.object.mode_set(mode='OBJECT')

						if old_active_object:

							context.scene.objects.active = old_active_object


		def __init__(self, operator, context, pipe):

			spline = pipe.data.splines.new('POLY')

			is_straight_pipe = random_integer(1, 100) < operator.straight

			if is_straight_pipe:

				self.depth(pipe, operator.depth)

				self.straight(spline, operator.height, operator.width)

			else:

				self.depth(pipe, operator.depth)

				self.bent(operator, context, pipe, spline)


		@staticmethod
		def depth(pipe, depth):

			depth = depth * 0.5

			pipe.location.y = random_float(-depth, depth)


		@staticmethod
		def straight(spline, height, width):

			width = width * 0.5

			base = spline.points[-1]
			base.co.x = random_float(-width, width)

			spline.points.add(count=1)

			spline.points[-1].co.x = base.co.x
			spline.points[-1].co.y = height


	def __init__(self, operator, context):

		seed(operator.seed)

		if operator.create_empty and not operator.convert:

			create.empty(operator, context)

		for index in range(operator.amount):

			pipe = create.pipe(operator, context, index)

			self.pipe(operator, context, pipe)


class create:


	@staticmethod
	def empty(operator, context):

		empty = bpy.data.objects.new(name='Pipes', object_data=None)

		context.scene.objects.link(empty)
		context.scene.objects.active = empty

		empty.empty_draw_type = 'CUBE'
		empty.location.z = operator.height * 0.5
		empty.scale = Vector((operator.width*0.5, operator.depth*0.5, operator.height*0.5))


	@staticmethod
	def pipe(operator, context, index):

		name = 'Pipe.{}'.format(str(index+1).zfill(len(str(operator.amount))))

		data = bpy.data.curves.new(name=name, type='CURVE')
		object = bpy.data.objects.new(name=name, object_data=data)
		context.scene.objects.link(object)

		if operator.create_empty and not operator.convert:

			pipe_object.select = True
			bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
			pipe_object.select = False

		data.fill_mode = 'NONE'
		data.bevel_depth = random_float(operator.min*0.5, operator.max*0.5)
		data.bevel_resolution = operator.surface

		object.rotation_euler.x = pi*0.5

		return object
