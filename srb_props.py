import bpy

class RenderBurstFilterSettings(bpy.types.PropertyGroup):
    rb_filter_enum: bpy.props.EnumProperty(
        name="Filter",
        description="Choose your destiny",
        items=[
            ("selected", "Selected Only", "Render selected only"),
            ("all", "All Cameras", "Render all cameras"),
        ],
        default='selected'
    )

    fallback_toggle: bpy.props.BoolProperty(
        name="GPU Fallback",
        description="Fallback to CPU if GPU render fails",
        default=False
    )
