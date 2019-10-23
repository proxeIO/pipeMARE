'''
This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    'name': 'Pipe Nightmare',
    'author': 'proxe',
    'version': (0, 3, 33),
    'blender': (2, 80, 0),
    'location': 'View 3D -> Add -> Curve -> Pipes',
    'description': 'Create random pipes within a region',
    'category': 'Object'
}

import bpy

from . import addon


def register():

    addon.register()


def unregister():

    addon.unregister()
