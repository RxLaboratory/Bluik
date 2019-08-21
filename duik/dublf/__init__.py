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

