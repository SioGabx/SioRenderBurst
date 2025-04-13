bl_info = {
    "name": "SioRenderBurst",
    "category": "Render",
    "blender": (4, 0, 0),
    "author": "SioGabx, Aidy Burrows, Gleb Alexandrov, Roman Alexandrov, CreativeShrimp.com",
    "version": (3, 0, 0),
    "description": "Render all cameras, one by one, and store results.",
    "support": "COMMUNITY",
}


if "bpy" in locals():
    import imp
    imp.reload(srb_utils)
    imp.reload(srb_ui)
    imp.reload(srb_props)
    imp.reload(srb_operators)
else:
    from . import srb_utils
    from . import srb_ui
    from . import srb_props
    from . import srb_operators

import bpy


def register():
    bpy.utils.register_class(srb_operators.RenderBurstOperator)
    bpy.utils.register_class(srb_props.RbFilterSettings)
    bpy.utils.register_class(srb_ui.RenderBurstPanel)
    bpy.utils.register_class(srb_ui.OBJECT_OT_RBButton)
    bpy.types.WindowManager.rb_filter = bpy.props.PointerProperty(type=srb_props.RbFilterSettings)
    bpy.types.TOPBAR_MT_render.append(srb_ui.menu_func)


def unregister():
    bpy.utils.unregister_class(srb_operators.RenderBurstOperator)
    bpy.utils.unregister_class(srb_props.RbFilterSettings)
    bpy.utils.unregister_class(srb_ui.RenderBurstPanel)
    bpy.utils.unregister_class(srb_ui.OBJECT_OT_RBButton)
    bpy.types.TOPBAR_MT_render.remove(srb_ui.menu_func)
    del bpy.types.WindowManager.rb_filter
