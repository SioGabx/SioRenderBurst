import bpy
from bpy.types import AddonPreferences
from bpy.props import BoolProperty


class RenderBurstAddonPreferences(AddonPreferences):
    # This must match the add-on name, use `__package__`
    # when defining this for add-on extensions or a sub-module of a python package.
    bl_idname = __package__
    print("bl_idname : " + __package__)
    GPUFallback: BoolProperty(
        name="Fallback to CPU if GPU render fails",
        default=False,
    )
    
    TrackToCamera: BoolProperty(
        name="Create and move a empty \"TrackToCameraTarget\" to camera location at render",
        default=False,
    )

    def draw(self, context):
        layout = self.layout
        #layout.label(text="This is a preferences view for our add-on")
        layout.prop(self, "GPUFallback")
        layout.prop(self, "TrackToCamera")
