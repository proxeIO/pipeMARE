import bpy

from bpy.utils import register_class, unregister_class


from . import operator, interface

classes = [
    operator.OBJECT_OT_pipe_nightmare,
]


def register():
    for cls in classes:
        register_class(cls)

    bpy.types.VIEW3D_MT_curve_add.append(interface.menu_entry)


def unregister():
    for cls in classes:
        unregister_class(cls)

    bpy.types.VIEW3D_MT_curve_add.remove(interface.menu_entry)
