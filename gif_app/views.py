import os
import subprocess
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from gif_app.models import Gif

BASE_DIR = settings.BASE_DIR
STATIC_DIR = os.path.join(BASE_DIR, "static", "banner")
STATIC_URL = settings.STATIC_URL


@api_view(['POST'])
@permission_classes([AllowAny])
def generate_gif(request):
    text = request.data.get("text", "")
    if not text:
        return JsonResponse({"error": "Text parameter is required"}, status=400)

    script_dir = os.path.join(BASE_DIR, "gif_app", "scripts")
    generate_script = os.path.join(script_dir, "generate.py")
    gif_script = os.path.join(script_dir, "gif.py")
    edit_script = os.path.join(script_dir, "edit.py")
    blender_path = r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"

    # Ensure static/banner directory exists
    if not os.path.exists(STATIC_DIR):
        os.makedirs(STATIC_DIR)

    # Validate script and Blender existence
    if not os.path.exists(generate_script):
        return JsonResponse({"error": "generate.py not found"}, status=500)

    if not os.path.exists(blender_path):
        return JsonResponse({"error": "Blender executable not found"}, status=500)

    try:
        # Run scripts sequentially
        subprocess.run(["python", generate_script, text], check=True)
        subprocess.run([blender_path, "-b", "--python", edit_script], check=True)
        subprocess.run(["python", gif_script], check=True)

        # Locate generated GIF
        gif_files = [f for f in os.listdir(STATIC_DIR) if f.endswith(".gif")]
        if not gif_files:
            return JsonResponse({"error": "GIF generation failed"}, status=500)

        latest_gif = max(gif_files, key=lambda f: os.path.getctime(os.path.join(STATIC_DIR, f)))
        gif_url = os.path.join(STATIC_URL, "banner", latest_gif).replace("\\", "/")

        return JsonResponse({"message": "Success", "file_path": gif_url})

    except subprocess.CalledProcessError as e:
        return JsonResponse({"error": f"Script execution failed: {str(e)}"}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_gifs(request):
    gifs = Gif.objects.all()
    gif_urls = [os.path.join(STATIC_URL, gif.default_gif.url) for gif in gifs if gif.default_gif]
    return JsonResponse({"data": gif_urls},status=200)