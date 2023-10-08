bl_info = {
    "name": "No Caps",
    "author": "diskutabel",
    "version": (1, 0, 4),
    "blender": (3, 6, 4),
    "location": "View3D > N",
    "description": "Automatically disables Caps Lock",
    "warning": "",
    "doc_url": "",
    "category": "System",
}


import bpy
from bpy.types import Panel, Operator
from bpy.utils import register_class, unregister_class

import ctypes
import threading


class Util:
    
    enabled = False
    
    disable_caps = 0
    
    global VK_CAPITAL
    VK_CAPITAL = 0x14
    
    global KEYEVENTF_EXTENDEDKEY
    KEYEVENTF_EXTENDEDKEY = 0x1
    global KEYEVENTF_KEYUP
    KEYEVENTF_KEYUP = 0x2
    
    def CAPSLOCK_STATE():
        return ctypes.windll.user32.GetKeyState(VK_CAPITAL)


class thread(threading.Thread): 
    def __init__(self, thread_name, thread_ID): 
        threading.Thread.__init__(self) 
        self.thread_name = thread_name 
        self.thread_ID = thread_ID 
 
    # helper function to execute the threads
    def run(self):
        while Util.enabled:
            CAPSLOCK = Util.CAPSLOCK_STATE()
            if ((CAPSLOCK) & 0xffff) != 0 and Util.enabled:
                ctypes.windll.user32.keybd_event(VK_CAPITAL, 0x45, KEYEVENTF_EXTENDEDKEY, 0)
                ctypes.windll.user32.keybd_event(VK_CAPITAL, 0x45, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)


class MenuePanel(bpy.types.Panel):
    bl_label = "NO CAPS"
    bl_idname = "OBJECT_PT_menue"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "No Caps"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator(EnableOperator.bl_idname, text="Enable", icon='OUTLINER_OB_FONT')
        row.operator(DisableOperator.bl_idname, text="Disable", icon='CANCEL')


class EnableOperator(bpy.types.Operator):
    bl_idname = "enable.1"
    bl_label = "Simple Enable Operator"


    def execute(self, context):
        
        if not Util.enabled:
            MenuePanel.bl_label = "No Caps"
            unregister_class(MenuePanel)
            register_class(MenuePanel)
            Util.enabled = True
            Util.disable_caps = thread("disable_caps", 1000)
            Util.disable_caps.start()

        return {'FINISHED'}


class DisableOperator(bpy.types.Operator):
    bl_idname = "disable.1"
    bl_label = "Simple Disable Operator"


    def execute(self, context):
       
        if Util.enabled:
            MenuePanel.bl_label = "NO CAPS"
            unregister_class(MenuePanel)
            register_class(MenuePanel)
            Util.enabled = False
            Util.disable_caps.join()
    
        return {'FINISHED'}


_classes = [
    MenuePanel,
    EnableOperator,
    DisableOperator
]


def register():
    for cls in _classes:
        register_class(cls)
    EnableOperator.execute(EnableOperator, 0)


def unregister():
    for cls in _classes:
        unregister_class(cls)
    Util.enabled = False
    Util.disable_caps.join()

if __name__ == "__main__":
    register()
