#====================== BEGIN GPL LICENSE BLOCK ======================
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#======================= END GPL LICENSE BLOCK ========================

# <pep8 compliant>

# The Duduf Blender Framework
# Useful tools to develop scripts in Blender

import bpy # pylint: disable=import-error
import time
from .rigging import DUBLF_rigging

class DUBLF_utils():
    """Utilitaries for Duduf's tools"""
    
    toolName = "Dublf"
    
    def log( self, log = "", time_start = 0 ):
        """Logs Duik activity"""
        t = time.time() - time_start
        print( " ".join( [ self.toolName , " (%.2f s):" % t , log ] ) )
        
    def showMessageBox( self, message = "", title = "Message Box", icon = 'INFO'):
        """Displays a simple message box"""
        def draw(self, context):
            self.layout.alert = True
            self.layout.label(text = message)
        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

