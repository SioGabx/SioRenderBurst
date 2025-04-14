import bpy

def set_device(device_type, compute_device):
    scene = bpy.context.scene
    if scene.render.engine == 'CYCLES':
        scene.cycles.device = device_type
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'CUDA' if device_type == 'GPU' else 'NONE'

def get_cycle_compute_device():
    prefs = bpy.context.preferences.addons['cycles'].preferences
    return prefs.compute_device_type


# BugFix: If cameras were bound to markers all cameras wouldn't get rendered.
markersDict = {}

# Make a note of markers in scene and any bound cameras, remove the bindings
def unbindMarkers():    
    scene = bpy.context.scene
    for marker in scene.timeline_markers:
        if marker.camera:
            markersDict[marker] = marker.camera
            marker.camera = None
            
# Put the bindings of cameras to markers back
def bindMarkers():   
    scene = bpy.context.scene     
    for marker in scene.timeline_markers:
        if marker in markersDict:
            marker.camera = markersDict[marker]


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
        print("Les nodes ne sont pas activés dans la scène.")


def show_message(message="", title="Message Box", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


def move_obj_to_collection(obj, collection_name):
    if collection_name not in bpy.data.collections:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)
        print(f"Collection '{collection_name}' created.")
    else:
        collection = bpy.data.collections[collection_name]

    collection.objects.link(obj)
    for col in obj.users_collection:
        if col != collection:
            col.objects.unlink(obj)