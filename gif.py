from PIL import Image
import os

image_folder = 'static/img/'
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
images = [Image.open(os.path.join(image_folder, f)) for f in image_files]
output_gif = 'static/output.gif'
images[0].save(output_gif, save_all=True, append_images=images[1:], duration=40, loop=0)