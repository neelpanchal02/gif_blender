import imageio
import os

image_folder = 'static/img/'
image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.png')])
images = []
for image_file in image_files:
    image_path = os.path.join(image_folder, image_file)
    images.append(imageio.imread(image_path))

output_gif = 'static/output.gif'
frame_rate = 25
duration_per_frame = 1 / frame_rate
imageio.mimsave(output_gif, images, duration=duration_per_frame)
print(f"GIF saved as {output_gif}")
