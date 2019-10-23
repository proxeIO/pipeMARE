import bpy
from math import pi
from mathutils import Vector
from random import seed, choice
from random import randint as random_integer
from random import uniform as random_float


class generate:


    def __init__(self, ot, context):
        seed(ot.seed)

        create.empty(ot, context)

        if ot.uniform:
            if ot.amount > 1:
                ot.depth_locations = [ot.depth * (index / (ot.amount - 1)) for index in range(ot.amount)]

        for index in range(ot.amount):
            thickness = random_float(ot.thickness_min, ot.thickness_max)

            pipe = create.pipe(ot, context, index, thickness)

            self.pipe(ot, context, pipe, index, thickness)


    class pipe:


        def __init__(self, ot, context, pipe, index, thickness):
            spline = pipe.data.splines.new('POLY')

            is_straight_pipe = random_integer(1, 100) <= ot.straight

            self.depth(ot, context, pipe, ot.depth * 0.5, index, thickness)

            if is_straight_pipe:

                self.straight(ot, pipe, spline, thickness)

            else:

                self.bent(ot, context, pipe, spline, thickness)

            self.align_profile(ot, context, pipe)


        class bent:


            def __init__(self, ot, context, pipe, spline, thickness):
                pipe_corners = self.get_corners(ot, context, pipe, spline, thickness)

                is_beveled = random_integer(1, 100) <= ot.bevel and ot.bevel_size > 0

                if is_beveled:

                    for index, point in enumerate(pipe_corners):

                        if index == 0:

                            create.point(spline, point)

                        elif index != len(pipe_corners) - 1:

                            if point[2]:

                                length_x = abs(point[0] - pipe_corners[index + 1][0])
                                length_y = abs(pipe_corners[index - 1][1] - point[1])

                                if min((length_x, length_y)) * (ot.bevel_size * 0.01) > thickness * 0.5:

                                    offset_y = -min((length_x, length_y)) * (ot.bevel_size * 0.01)
                                    offset_x = offset_y if point[3] else -offset_y

                                    create.point(spline, point, offset_y=offset_y)
                                    create.point(spline, point, offset_x=offset_x)

                                    point[0] += offset_x

                                else:

                                    create.point(spline, point)

                            else:

                                length_x = abs(pipe_corners[index - 1][0] - point[0])
                                length_y = abs(point[1] - pipe_corners[index + 1][1])

                                if min((length_x, length_y)) * (ot.bevel_size * 0.01) > thickness * 0.5:

                                    offset_y = min((length_x, length_y)) * (ot.bevel_size * 0.01)
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


            def get_corners(self, ot, context, pipe, spline, thickness):
                keep_inside = generate.pipe.keep_inside

                spline.points[-1].co.x = keep_inside(random_float(-ot.width * 0.5, ot.width * 0.5), thickness, ot.width * 0.5)

                last_x = spline.points[-1].co.x
                last_y = 0.0

                first_pass = True

                pipe_corners = [[last_x, last_y]]

                while last_y < ot.heigth:

                    if first_pass:

                        coord_y = keep_inside(last_y + random_float(ot.length_y_min, ot.length_y_max) * 0.5 , thickness, ot.heigth)

                        first_pass = False

                    else:

                        coord_y = keep_inside(last_y + random_float(ot.length_y_min, ot.length_y_max) , thickness, ot.heigth)

                    if coord_y + min(ot.length_y_min, ot.length_y_max) * 0.5 > ot.heigth:

                        pipe_corners.append([last_x, ot.heigth])

                        break

                    length_x_min = ot.length_x_min
                    length_x_max = ot.length_x_max

                    if last_x - length_x_min - thickness <= -ot.width * 0.5:

                        left = False

                    elif last_x + length_x_min + thickness >= ot.width * 0.5:

                        left = True

                    else:

                        left = choice([True, False])

                    thickness = -thickness if left else thickness
                    length_x_min = -length_x_min if left else length_x_min
                    length_x_max = -length_x_max if left else length_x_max

                    coord_x = keep_inside(last_x + random_float(length_x_min, length_x_max), thickness, ot.width * 0.5)

                    pipe_corners.append([last_x, coord_y, True, left])

                    last_x = coord_x
                    last_y = coord_y

                    pipe_corners.append([last_x, last_y, False, left])

                return pipe_corners


        @staticmethod
        def keep_inside(coordinate, thickness, limit):
            left = True if coordinate < 0.0 else False

            coordinate = abs(coordinate)
            thickness = abs(thickness)

            if coordinate + thickness > limit:

                coordinate = coordinate - thickness - abs(coordinate - limit)

            coordinate = -coordinate if left else coordinate

            return coordinate


        @staticmethod
        def align_profile(ot, context, pipe):
            point_origin = pipe.data.splines[0].points[0].co

            # cursor = context.scene.cursor

            pipe.data.bevel_object.location = Vector((ot.location.x + point_origin.x, pipe.location.y, ot.location.z))


        def depth(self, ot, context, pipe, depth, index, thickness):
            pipe.location.y += self.keep_inside(random_float(-depth, depth), thickness, depth)

            if ot.uniform:

                pipe.location.y = ot.location.y

                if ot.amount > 1:

                    pipe.location.y += ot.depth_locations[index] - ot.depth * 0.5


        def straight(self, ot, pipe, spline, thickness):
            spline.points[0].co.x = self.keep_inside(random_float(-ot.width * 0.5, ot.width * 0.5), thickness, ot.width * 0.5)

            spline.points.add(count=1)

            spline.points[-1].co.x = spline.points[-2].co.x
            spline.points[-1].co.y = ot.heigth


class create:


    class profile:


        def __new__(self, ot, context, pipe, thickness):
            split = random_integer(1, 100) <= ot.split

            pipe_profile = create.curve(ot, context, pipe.name+'-profile')

            self.pipe(ot, context, pipe_profile, split, thickness)
            self.set_dimensions(ot, pipe_profile, thickness)

            return pipe_profile


        class pipe:


            def __init__(self, ot, context, pipe_profile, split, thickness):
                type = 'single' if thickness < ot.thickness_max * 0.75 else None

                if split:
                    self.split(pipe_profile, type=type)

                else:
                    self.standard(pipe_profile)


            class split:


                def __init__(self, pipe_profile, type=None):
                    type = ['single', 'double'][random_integer(0, 1)] if not type else type
                    getattr(self, type)(pipe_profile)


                class single:


                    def __init__(self, pipe_profile):
                        spline1 = pipe_profile.data.splines.new('BEZIER')
                        spline1.use_cyclic_u = True

                        spline2 = pipe_profile.data.splines.new('BEZIER')
                        spline2.use_cyclic_u = True

                        type = ['type1', 'type2', 'type3']
                        getattr(self, type[random_integer(0, 2)])(pipe_profile, spline1, spline2)


                    @staticmethod
                    def type1(pipe_profile, spline1, spline2):

                        coordinates1 = [
                            [-0.4304378628730774, -0.16793787479400635],
                            [-0.4304378628730774, 0.16793787479400635],
                            [-0.09456212818622589, 0.16793787479400635],
                            [-0.09456212818622589, -0.16793787479400635],
                        ]

                        coordinates2 = [
                            [0.09456212818622589, -0.16793787479400635],
                            [0.09456212818622589, 0.16793787479400635],
                            [0.4304378628730774, 0.16793787479400635],
                            [0.4304378628730774, -0.16793787479400635],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)


                    @staticmethod
                    def type2(pipe_profile, spline1, spline2):

                        coordinates1 = [
                            [-0.4267767071723938, -0.1767767071723938],
                            [-0.4267767071723938, 0.1767767071723938],
                            [-0.0732232928276062, 0.1767767071723938],
                            [-0.0732232928276062, -0.1767767071723938],
                        ]

                        coordinates2 = [
                            [0.17991751432418823, -0.13258254528045654],
                            [0.17991751432418823, 0.13258254528045654],
                            [0.44508254528045654, 0.13258254528045654],
                            [0.44508254528045654, -0.13258254528045654],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)


                    @staticmethod
                    def type3(pipe_profile, spline1, spline2):

                        coordinates1 = [
                            [0.4892767667770386, 0.1767767071723938],
                            [0.4892767667770386, -0.1767767071723938],
                            [0.13572333753108978, -0.1767767071723938],
                            [0.13572333753108978, 0.1767767071723938],
                        ]

                        coordinates2 = [
                            [-0.11741745471954346, 0.13258254528045654],
                            [-0.11741745471954346, -0.13258254528045654],
                            [-0.38258248567581177, -0.13258254528045654],
                            [-0.38258248567581177, 0.13258254528045654],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)


                class double:


                    def __init__(self, pipe_profile):

                        spline1 = pipe_profile.data.splines.new('BEZIER')
                        spline1.use_cyclic_u = True

                        spline2 = pipe_profile.data.splines.new('BEZIER')
                        spline2.use_cyclic_u = True

                        spline3 = pipe_profile.data.splines.new('BEZIER')
                        spline3.use_cyclic_u = True

                        type = ['type1', 'type2', 'type3', 'type4']
                        getattr(self, type[random_integer(0, 3)])(pipe_profile, spline1, spline2, spline3)

                    @staticmethod
                    def type1(pipe_profile, spline1, spline2, spline3):

                        coordinates1 = [
                            [-0.1060660183429718, -0.1060660183429718],
                            [-0.1060660183429718, 0.1060660183429718],
                            [0.1060660183429718, 0.1060660183429718],
                            [0.1060660183429718, -0.1060660183429718],
                        ]

                        coordinates2 = [
                            [0.24393399059772491, -0.1060660183429718],
                            [0.24393399059772491, 0.1060660183429718],
                            [0.4560660123825073, 0.1060660183429718],
                            [0.4560660123825073, -0.1060660183429718],
                        ]

                        coordinates3 = [
                            [-0.4560660123825073, -0.1060660183429718],
                            [-0.4560660123825073, 0.1060660183429718],
                            [-0.24393399059772491, 0.1060660183429718],
                            [-0.24393399059772491, -0.1060660183429718],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates3):

                            create.point(spline3, point, index=index, bezier=True)


                    @staticmethod
                    def type2(pipe_profile, spline1, spline2, spline3):

                        coordinates1 = [
                            [-0.2121320366859436, -0.2121320366859436],
                            [-0.2121320366859436, 0.2121320366859436],
                            [0.2121320366859436, 0.2121320366859436],
                            [0.2121320366859436, -0.2121320366859436],
                        ]

                        coordinates2 = [
                            [0.37196701765060425, -0.0530330091714859],
                            [0.37196701765060425, 0.0530330091714859],
                            [0.47803300619125366, 0.0530330091714859],
                            [0.47803300619125366, -0.0530330091714859],
                        ]

                        coordinates3 = [
                            [-0.47803300619125366, -0.0530330091714859],
                            [-0.47803300619125366, 0.0530330091714859],
                            [-0.37196701765060425, 0.0530330091714859],
                            [-0.37196701765060425, -0.0530330091714859],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates3):

                            create.point(spline3, point, index=index, bezier=True)


                    @staticmethod
                    def type3(pipe_profile, spline1, spline2, spline3):

                        coordinates1 = [
                            [-0.41213202476501465, -0.2121320366859436],
                            [-0.41213202476501465, 0.2121320366859436],
                            [0.012132033705711365, 0.2121320366859436],
                            [0.012132033705711365, -0.2121320366859436],
                        ]

                        coordinates2 = [
                            [0.37196701765060425, -0.0530330091714859],
                            [0.37196701765060425, 0.0530330091714859],
                            [0.47803300619125366, 0.0530330091714859],
                            [0.47803300619125366, -0.0530330091714859],
                        ]

                        coordinates3 = [
                            [0.17196696996688843, -0.0530330091714859],
                            [0.17196696996688843, 0.0530330091714859],
                            [0.27803295850753784, 0.0530330091714859],
                            [0.27803295850753784, -0.0530330091714859],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates3):

                            create.point(spline3, point, index=index, bezier=True)


                    @staticmethod
                    def type4(pipe_profile, spline1, spline2, spline3):

                        coordinates1 = [
                            [0.41213202476501465, 0.2121320366859436],
                            [0.41213202476501465, -0.2121320366859436],
                            [-0.012132033705711365, -0.2121320366859436],
                            [-0.012132033705711365, 0.2121320366859436],
                        ]

                        coordinates2 = [
                            [-0.37196701765060425, 0.0530330091714859],
                            [-0.37196701765060425, -0.0530330091714859],
                            [-0.47803300619125366, -0.0530330091714859],
                            [-0.47803300619125366, 0.0530330091714859],
                        ]

                        coordinates3 = [
                            [-0.17196696996688843, 0.0530330091714859],
                            [-0.17196696996688843, -0.0530330091714859],
                            [-0.27803295850753784, -0.0530330091714859],
                            [-0.27803295850753784, 0.0530330091714859],
                        ]

                        for index, point in enumerate(coordinates1):

                            create.point(spline1, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates2):

                            create.point(spline2, point, index=index, bezier=True)

                        for index, point in enumerate(coordinates3):

                            create.point(spline3, point, index=index, bezier=True)


            @staticmethod
            def standard(pipe_profile):

                spline = pipe_profile.data.splines.new('BEZIER')
                spline.use_cyclic_u = True

                base = 0.3535533547401428

                coordinates = [[-base, -base], [-base, base], [base, base], [base, -base]]

                for index, point in enumerate(coordinates):

                    create.point(spline, point, index=index, bezier=True)


        @staticmethod
        def set_dimensions(ot, pipe_profile, thickness):

            pipe_profile.matrix_world[0][0] = thickness
            pipe_profile.matrix_world[1][1] = thickness


    def curve(ot, context, name):

        data = bpy.data.curves.new(name=name, type='CURVE')
        curve = bpy.data.objects.new(name=name, object_data=data)
        context.scene.collection.objects.link(curve)

        create.set_parent(curve)

        curve.data.fill_mode = 'NONE'

        return curve


    def empty(ot, context):

        empty = bpy.data.objects.new(name='Pipes', object_data=None)

        context.scene.collection.objects.link(empty)
        context.view_layer.objects.active = empty

        empty.empty_display_type = 'CUBE'
        empty.location = ot.location
        empty.location.z += ot.heigth * 0.5
        empty.scale = Vector((ot.width * 0.5, ot.depth * 0.5, ot.heigth * 0.5))

        ot.empty = empty


    def point(spline, point, offset_x=0.0, offset_y=0.0, index=0, bezier=False):

        if bezier:

            if index == 0:

                spline.bezier_points[0].co.x = point[0] + offset_x
                spline.bezier_points[0].co.y = point[1] + offset_y
                spline.bezier_points[0].handle_left_type = 'AUTO'
                spline.bezier_points[0].handle_right_type = 'AUTO'

            else:

                spline.bezier_points.add(count=1)

                spline.bezier_points[-1].co.x = point[0] + offset_x
                spline.bezier_points[-1].co.y = point[1] + offset_y
                spline.bezier_points[-1].handle_left_type = 'AUTO'
                spline.bezier_points[-1].handle_right_type = 'AUTO'

        else:

            spline.points.add(count=1)

            spline.points[-1].co.x = point[0] + offset_x
            spline.points[-1].co.y = point[1] + offset_y


    def set_parent(pipe):

        bpy.ops.object.select_all(action='DESELECT')

        pipe.select_set(True)

        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        pipe.select_set(False)


    def pipe(ot, context, index, thickness):
        name = F'Pipe.{str(index + 1).zfill(len(str(ot.amount)))}'

        pipe = create.curve(ot, context, name)

        pipe.data.bevel_object = create.profile(ot, context, pipe, thickness)
        pipe.data.bevel_object.data.resolution_u = ot.surface

        pipe.rotation_euler.x = pi * 0.5
        pipe.location = ot.location

        return pipe
