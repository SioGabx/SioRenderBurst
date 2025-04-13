import bpy

def set_device(device_type):
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.device = device_type
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA' if device_type == 'GPU' else 'NONE'

def update_output_paths(camName):
    scene = bpy.context.scene
    if scene.use_nodes and scene.node_tree:
        count = 0
        for node in scene.node_tree.nodes:
            if node.type == 'OUTPUT_FILE':  # Vérifie le type du node
                if node.file_slots:
                    node.file_slots[0].path = camName
                    count += 1
        print(f"{count} node(s) 'CompositorNodeOutputFile' mis à jour.")
    else:
        print("ERREUR : Les nodes ne sont pas activés dans la scène.")


def show_message(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

