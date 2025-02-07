import os
import imageio.v2 as imageio  # Fix deprecation warning

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
input_dir = os.path.join(project_root, "static", "banner" ,"img")
output_gif = os.path.join(project_root, "static","banner" , "output.gif")

# Get frame files
frames = sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".png")])

# Create GIF
if frames:
    with imageio.get_writer(output_gif, mode="I", duration=0.1) as writer:
        for frame in frames:
            writer.append_data(imageio.imread(frame))  # Use new syntax
    print(f"GIF saved as {output_gif}")
else:
    print("No frames found to create GIF.")
