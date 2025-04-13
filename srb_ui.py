import bpy


def menu_func(self, context):
    self.layout.separator()
    self.layout.operator("render.render_burst", icon="RENDERLAYERS")

class RenderBurstPanel(bpy.types.Panel):
    bl_label = "Render Burst"
    bl_idname = "RENDER_PT_render_burst"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager

        layout.prop(wm.rb_filter, "rb_filter_enum", expand=True)
        layout.prop(wm.rb_filter, "fallback_toggle")
        layout.operator("rb.render_button", text='Render!')


class OBJECT_OT_RBButton(bpy.types.Operator):
    bl_idname = "rb.render_button"
    bl_label = "Render"

    def execute(self, context):
        render = context.scene.render

        if not render.filepath:
            self.report({"ERROR"}, 'Output path not defined in render settings.')
            return {'CANCELLED'}

        if render.image_settings.file_format in {'FFMPEG', 'AVI_JPEG', 'AVI_RAW', 'FRAMESERVER'}:
            self.report({"ERROR"}, 'Animation formats are not supported.')
            return {'CANCELLED'}

        bpy.ops.render.render_burst()
        return {'FINISHED'}
