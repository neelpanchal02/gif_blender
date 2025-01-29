import bpy
import os

# Enable GPU rendering
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'  # Use 'OPENCL' for AMD
bpy.context.scene.cycles.device = 'GPU'

blend_file_path = "static/blenderFile.blend"
bpy.ops.wm.open_mainfile(filepath=blend_file_path)

image_path = "/var/www/html/gif_blender/static/output.png"
image_texture = bpy.data.images.load(image_path)

material = bpy.data.materials.new(name="Material")
material.use_nodes = True
nodes = material.node_tree.nodes
for node in nodes:
    nodes.remove(node)

principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
image_texture_node = nodes.new(type="ShaderNodeTexImage")
image_texture_node.image = image_texture
material.node_tree.links.new(image_texture_node.outputs['Color'], principled_bsdf.inputs['Base Color'])
material.node_tree.links.new(image_texture_node.outputs['Alpha'], principled_bsdf.inputs['Alpha'])
material_output_node = nodes.new(type="ShaderNodeOutputMaterial")
material.node_tree.links.new(principled_bsdf.outputs['BSDF'], material_output_node.inputs['Surface'])

obj = bpy.context.scene.objects.get('file')
if obj.type == 'MESH':
    obj.data.materials.clear()
    obj.data.materials.append(material)

# Set output directory
output_dir = "/var/www/html/gif_blender/static/img"
os.makedirs(output_dir, exist_ok=True)
output_file_path = os.path.join(output_dir, "frame_####.png")

bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = output_file_path

# **Enable GPU for rendering**
bpy.context.scene.cycles.samples = 128  # Adjust based on GPU capability
bpy.ops.render.render(animation=True)
