import bpy

from bpy.types import Operator
from bpy.props import BoolProperty, FloatProperty

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
    default = default['preview']
  )

  bounds = BoolProperty(
    name = 'Bounds',
    description = 'Display the bounds of the generated pipes in the 3D View',
    default = default['bounds']
  )

  pipes = BoolProperty(
    name = 'Pipes',
    description = 'Display the generated pipes in the 3D View',
    default = default['pipes']
  )

  # width
  # height
  # length_x
  # length_y
  # straight
  # decoration
  # rail
  # extra
  # bevel


  def check(self, context):

    return True


  def draw(self, context):

    interface.draw(self, context)


  def execute(self, context):

    return {'FINISHED'}


  def invoke(self, context, event):

    context.window_manager.invoke_props_dialog(self, width=250)
