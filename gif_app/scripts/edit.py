import bpy
import os

# Get absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
blend_file_path = os.path.join(project_root, "static","banner" ,"blenderFile.blend")
image_path = os.path.join(project_root, "static","banner" , "output.png")
output_dir = os.path.join(project_root, "static","banner" , "img")

# Ensure paths exist
if not os.path.exists(image_path):
    raise FileNotFoundError(f"Error: Image file not found at {image_path}")

if not os.path.exists(blend_file_path):
    raise FileNotFoundError(f"Error: Blender file not found at {blend_file_path}")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Load Blender file
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

# Load image texture
image_texture = bpy.data.images.load(image_path)

# Create new material
material = bpy.data.materials.new(name="Material")
material.use_nodes = True

# Clear existing nodes
nodes = material.node_tree.nodes
for node in nodes:
    nodes.remove(node)

# Add Principled BSDF and Image Texture Node
principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
image_texture_node = nodes.new(type="ShaderNodeTexImage")
image_texture_node.image = image_texture

# Connect nodes
material.node_tree.links.new(image_texture_node.outputs['Color'], principled_bsdf.inputs['Base Color'])
material.node_tree.links.new(image_texture_node.outputs['Alpha'], principled_bsdf.inputs['Alpha'])

# Add Material Output Node
material_output_node = nodes.new(type="ShaderNodeOutputMaterial")
material.node_tree.links.new(principled_bsdf.outputs['BSDF'], material_output_node.inputs['Surface'])

# Get the object and assign the material
obj = bpy.context.scene.objects.get('file')

if obj and obj.type == 'MESH':
    obj.data.materials.clear()
    obj.data.materials.append(material)
else:
    raise ValueError("Error: Object 'file' not found or is not a mesh.")

# Set output file path for rendering
output_file_path = os.path.join(output_dir, "frame_####.png")
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = output_file_path

# Render animation
bpy.ops.render.render(animation=True)
