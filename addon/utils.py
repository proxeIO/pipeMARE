import bpy
from math import pi
from mathutils import Vector
from random import seed
from random import randint as random_integer
from random import uniform as random_float


class generate:


	class pipe:


		def __init__(self, operator, context, pipe):

			spline = pipe.data.splines.new('POLY')

			is_straight_pipe = random_integer(1, 100) < operator.straight

			if is_straight_pipe:

				self.straight(operator, pipe, spline)

			else:

				self.bent(operator, context, pipe, spline)


		@staticmethod
		def keep_inside(coordinate, thickness_offset, limit):

			if coordinate + thickness_offset > limit:

				coordinate = coordinate - thickness_offset - (coordinate - limit)

			elif coordinate - thickness_offset < -limit:

				coordinate = coordinate + thickness_offset - (coordinate + limit)

			return coordinate


		def depth(self, pipe, depth):

			pipe.location.y = self.keep_inside(random_float(-depth, depth), pipe.data.bevel_depth, depth)


		def straight(self, operator, pipe, spline):

			self.depth(pipe, operator.depth*0.5)

			spline.points[-1].co.x = self.keep_inside(random_float(-operator.width*0.5, operator.width*0.5), pipe.data.bevel_depth, operator.width*0.5)

			spline.points.add(count=1)

			spline.points[-1].co.x = spline.points[-2].co.x
			spline.points[-1].co.y = operator.height


		def bent(self, operator, context, pipe, spline):

			self.depth(pipe, operator.depth*0.5)

			spline.points[-1].co.x = self.keep_inside(random_float(-operator.width*0.5, operator.width*0.5), pipe.data.bevel_depth, operator.width*0.5)

			last_y = 0.0
			last_x = spline.points[-1].co.x

			first_pass = True

			beveled_pipe = random_integer(1, 100) < operator.bevel

			while last_y < operator.height - pipe.data.bevel_depth:

				coord_x = self.keep_inside(last_x+random_float(-operator.length_x, operator.length_x), pipe.data.bevel_depth, operator.width*0.5)
				coord_y = self.keep_inside(last_y+random_float(operator.length_y*0.1, operator.length_y), pipe.data.bevel_depth, operator.height)

				spline.points.add(count=2)

				spline.points[-2].co.x = last_x
				spline.points[-2].co.y = coord_y
				spline.points[-1].co.x = coord_x
				spline.points[-1].co.y = coord_y

				last_x = coord_x
				last_y = coord_y

			else:

				spline.points.add(count=1)
				spline.points[-1].co.x = last_x
				spline.points[-1].co.y = operator.height


		@staticmethod
		def bevel():

			pass


		@staticmethod
		def delete_point(context, pipe, point):

			point.select = True

			old_active_object = bpy.data.objects[context.active_object.name] if context.active_object else None

			context.scene.objects.active = pipe

			bpy.ops.object.mode_set(mode='EDIT')
			bpy.ops.curve.delete(type='VERT')
			bpy.ops.object.mode_set(mode='OBJECT')

			if old_active_object:

				context.scene.objects.active = old_active_object


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

			object.select = True
			bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
			object.select = False

		data.fill_mode = 'NONE'
		data.bevel_depth = random_float(operator.min*0.5, operator.max*0.5)
		data.bevel_resolution = operator.surface

		object.rotation_euler.x = pi * 0.5

		return object
