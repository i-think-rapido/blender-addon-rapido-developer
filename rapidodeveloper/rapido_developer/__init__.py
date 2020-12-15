# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****


bl_info = {
    "name": "Rapido Developer",
    "author": "romdisc",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    #"location": "3D View > Properties> Auto-Rig Pro",
    "description": "Tool for Easy Blender Addon Development",
    #"tracker_url": "http://lucky3d.fr/auto-rig-pro/doc/bug_report.html",    
    "category": "Development"}

if "bpy" in locals():
    import importlib
    if "rapido_developer" in locals():
        importlib.reload(rapido_developer)

import bpy
import os
#import script files
from . import rapido_developer


def register():  
    rapido_developer.register()

def unregister():
    rapido_developer.unregister()

if __name__ == "__main__":
    register()

