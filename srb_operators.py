import bpy
import os

from .srb_utils import *

class RenderBurstOperator(bpy.types.Operator):
    bl_idname = "render.render_burst"
    bl_label = "Render Burst"
    
    _timer = None
    shots = []
    CatchRenderCancel = False
    stop = False
    rendering = False
    path = "//"
    original_device = None
    original_compute_device = get_cycle_compute_device()
    GPU_compute_device = 'CUDA' if original_compute_device == 'NONE' else original_compute_device
    fallback_enabled = True

    def pre(self, dummy, thrd=None):
        self.rendering = True
        print(f"Starting render of camera \"{self.shots[0]}\" with {self.context.scene.cycles.device}.")

    def post(self, dummy, thrd=None):
        if len(self.shots) == 0:
            print("There is no camera left")
            return
        print(f"There is {len(self.shots)} in queue.")
        current_shot = self.shots[0]
        path = self.resolve_path(self.path, current_shot)
        if self.original_device == "GPU":
            if os.path.exists(path):
                print(f"Render found for {current_shot} at {path}. Deleting queue from list.")
                self.shots.pop(0)
                if self.fallback_enabled :
                    set_device(self.original_device, self.GPU_compute_device)
            else:
                print(f"File missing for {current_shot} à {path}. Retry with CPU ?.")
                if bpy.context.scene.cycles.device == "CPU":
                    print(f"Render failed with CPU for {current_shot}. Deleting queue from list.")
                    self.shots.pop(0)
                else:
                    # Current device is GPU, try render with CPU
                    if self.fallback_enabled :
                        print(f"Retry render with CPU this time.")
                        set_device("CPU", self.GPU_compute_device)
                        CatchRenderCancel = True
                    else:
                        print(f"Don't retry with CPU")
                        self.shots.pop(0)
        else:
            #Already rendered with CPU
            self.shots.pop(0)
        self.rendering = False        

    def cancelled(self, dummy, thrd=None):
        if not self.CatchRenderCancel:
            self.stop = True
            print(f"Render cancelled.")
        print(f"Render cancel avoid.")
        self.CatchRenderCancel = False

        
    def execute(self, context):
        scene = context.scene
        self.stop = False
        self.rendering = False
        self.original_device = scene.cycles.device
        self.fallback_enabled = context.window_manager.rb_filter.fallback_toggle
        self.context = context
        wm = context.window_manager

        if wm.rb_filter.rb_filter_enum == 'selected':
            self.shots = [obj.name for obj in context.selected_objects if obj.type == 'CAMERA' and obj.visible_get()]
        else:
            self.shots = [obj.name for obj in context.visible_objects if obj.type == 'CAMERA' and obj.visible_get()]

        if not self.shots and scene.camera:
            print(f"Aucune caméra sélectionnée ou visible. Utilisation de la caméra active : {scene.camera.name}")
            self.shots.append(scene.camera.name)

        if not self.shots:
            self.report({"WARNING"}, 'No cameras found to render.')
            return {"CANCELLED"}

        if self.pre not in bpy.app.handlers.render_pre:
            bpy.app.handlers.render_pre.append(self.pre)
        if self.post not in bpy.app.handlers.render_post:
            bpy.app.handlers.render_post.append(self.post)
        if self.cancelled not in bpy.app.handlers.render_cancel:
            bpy.app.handlers.render_cancel.append(self.cancelled)

        self._timer = wm.event_timer_add(1, window=context.window)
        wm.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        if event.type != 'TIMER':
            return {'PASS_THROUGH'}

        if not self.shots or self.stop:
            self.cleanup(context)
            return {'FINISHED'}

        if not self.rendering:
            cam_name = self.shots[0]
            cam_obj = bpy.data.objects.get(cam_name)
            if not cam_obj:
                # Camera was deleted 
                self.shots.pop(0)
                return {'PASS_THROUGH'}

            context.scene.camera = cam_obj
            path = self.resolve_path(self.path, cam_name)
            context.scene.render.filepath = path

            update_output_paths(cam_name)
            # Render !
            bpy.ops.render.render("INVOKE_DEFAULT", write_still=True)
           
        return {'PASS_THROUGH'}

    def resolve_path(self, path, cameraName):
        fpath = bpy.context.scene.render.filepath
        is_relative_path = fpath.startswith("//")

        if is_relative_path:
            fpath = bpy.path.abspath(fpath)

        path = os.path.dirname(fpath).rstrip("/\\") + "/"
        return path + cameraName + bpy.context.scene.render.file_extension

    def cleanup(self, context):
        handlers = bpy.app.handlers
        for hlist, handler in [
            (handlers.render_pre, self.pre),
            (handlers.render_post, self.post),
            (handlers.render_cancel, self.cancelled)
        ]:
            if handler in hlist:
                hlist.remove(handler)

        context.window_manager.event_timer_remove(self._timer)
        set_device(self.original_device, self.original_compute_device)
