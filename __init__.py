bl_info = {
    "name": "SioRenderBurst",
    "category": "Render",
    "blender": (4, 0, 0),
    "author": "SioGabx, Aidy Burrows, Gleb Alexandrov, Roman Alexandrov, creativeshrimp.com",
    "version": (3, 0, 0),
    "description": "Render selected or all cameras, one by one, and store results.",
    "support": "COMMUNITY",
}


if "bpy" in locals():
    import imp
    imp.reload(srb_utils)
    imp.reload(srb_ui)
    imp.reload(srb_props)
    imp.reload(srb_operators)
    imp.reload(srb_preferences)
else:
    from . import srb_utils
    from . import srb_ui
    from . import srb_props
    from . import srb_operators
    from . import srb_preferences

import bpy


def register():
    bpy.utils.register_class(srb_preferences.RenderBurstAddonPreferences)
    bpy.utils.register_class(srb_operators.RenderBurstOperator)
    bpy.utils.register_class(srb_props.RenderBurstFilterSettings)
    bpy.utils.register_class(srb_ui.RenderBurstPanel)
    bpy.utils.register_class(srb_ui.OBJECT_OT_RBButton)
    bpy.types.WindowManager.rb_filter = bpy.props.PointerProperty(type=srb_props.RenderBurstFilterSettings)
    bpy.context.window_manager.rb_filter.fallback_toggle = bpy.context.preferences.addons.get(__package__).preferences.GPUFallback
    bpy.types.TOPBAR_MT_render.append(srb_ui.menu_func)


def unregister():
    bpy.utils.unregister_class(srb_preferences.RenderBurstAddonPreferences)
    bpy.utils.unregister_class(srb_operators.RenderBurstOperator)
    bpy.utils.unregister_class(srb_props.RenderBurstFilterSettings)
    bpy.utils.unregister_class(srb_ui.RenderBurstPanel)
    bpy.utils.unregister_class(srb_ui.OBJECT_OT_RBButton)
    bpy.types.TOPBAR_MT_render.remove(srb_ui.menu_func)
    del bpy.types.WindowManager.rb_filter
