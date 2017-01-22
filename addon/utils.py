import bpy
from math import pi
from mathutils import Vector
from random import seed, choice
from random import randint as random_integer
from random import uniform as random_float


class generate:


	class pipe:


		def __init__(self, operator, context, pipe):

			spline = pipe.data.splines.new('POLY')

			is_straight_pipe = random_integer(1, 100) < operator.straight

			if not operator.uniform:

				self.depth(operator, pipe, operator.depth*0.5)

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


		def depth(self, operator, pipe, depth):

			pipe.location.y += self.keep_inside(random_float(-depth, depth), pipe.data.bevel_depth, depth)


		def straight(self, operator, pipe, spline):

			spline.points[-1].co.x = self.keep_inside(random_float(-operator.width*0.5, operator.width*0.5), pipe.data.bevel_depth, operator.width*0.5)

			spline.points.add(count=1)

			spline.points[-1].co.x = spline.points[-2].co.x
			spline.points[-1].co.y = operator.height


		def bent(self, operator, context, pipe, spline):

			spline.points[-1].co.x = self.keep_inside(random_float(-operator.width*0.5, operator.width*0.5), pipe.data.bevel_depth, operator.width*0.5)

			last_x = spline.points[-1].co.x
			last_y = 0.0

			pipe_corners = [[last_x, last_y]]

			while last_y < operator.height - pipe.data.bevel_depth:

				left = choice([True, False])
				thickness = -pipe.data.bevel_depth if left else pipe.data.bevel_depth
				length_x = -operator.length_x if left else operator.length_x
				length_x += thickness*2
				coord_x = self.keep_inside(last_x+random_float(thickness*2, length_x), pipe.data.bevel_depth, operator.width*0.5)
				coord_y = self.keep_inside(last_y+random_float(pipe.data.bevel_depth*2, operator.length_y+pipe.data.bevel_depth*2), pipe.data.bevel_depth, operator.height)

				pipe_corners.append([last_x, coord_y, True, left])

				last_x = coord_x
				last_y = coord_y

				pipe_corners.append([last_x, last_y, False, left])

			else:

				pipe_corners.append([last_x, operator.height])

				is_beveled = random_integer(1, 100) < operator.bevel

				if is_beveled:

					for index, point in enumerate(pipe_corners):

						if index == 0:

							create.point(spline, point)

						elif index != len(pipe_corners) - 1:

							if point[2]:

								length_x = abs(point[0]-pipe_corners[index+1][0])
								length_y = abs(pipe_corners[index-1][1]-point[1])

								if min((length_x, length_y)) * 0.25 > pipe.data.bevel_depth:

									offset_y = -min((length_x, length_y))*0.25
									offset_x = offset_y if point[3] else -offset_y

									create.point(spline, point, offset_y=offset_y)
									create.point(spline, point, offset_x=offset_x)

									point[0] += offset_x

								else:

									create.point(spline, point)

							else:

								length_x = abs(pipe_corners[index-1][0]-point[0])
								length_y = abs(point[1]-pipe_corners[index+1][1])

								if min((length_x, length_y)) * 0.25 > pipe.data.bevel_depth:

									offset_y = min((length_x, length_y))*0.25
									offset_x = offset_y if point[3] else -offset_y

									create.point(spline, point, offset_x=offset_x)
									create.point(spline, point, offset_y=offset_y)

									point[1] += offset_y

								else:

									create.point(spline, point)

						else:

							create.point(spline, point)

				else:

					for point in pipe_corners:

						create.point(spline, point)

			flip = choice([True, False])

			if flip:

				pipe.rotation_euler.x = -pi * 0.5
				pipe.location.z += operator.height


	def __init__(self, operator, context):

		seed(operator.seed)

		if operator.create_empty and not operator.convert:

			create.empty(operator, context)

		if operator.uniform:

			if operator.amount == 1:

				operator.depth_locations.append(0.0)

			else:

				operator.depth_locations = [operator.depth*(index/(operator.amount-1)) for index in range(operator.amount)]

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
		empty.location = context.space_data.cursor_location
		empty.location.z += operator.height * 0.5
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
		object.location = context.space_data.cursor_location

		if operator.uniform:

			if operator.amount > 1:

				object.location.y += operator.depth_locations[index] - operator.depth * 0.5

		return object


	@staticmethod
	def point(spline, point, offset_x=0.0, offset_y=0.0):

		spline.points.add(count=1)

		spline.points[-1].co.x = point[0] + offset_x
		spline.points[-1].co.y = point[1] + offset_y
