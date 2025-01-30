import subprocess
import os
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

BASE_DIR = settings.BASE_DIR


def index(request):
    return render(request, "index.html")


@csrf_exempt
def generate(request):
    if request.method == "POST":
        text = request.POST.get("text", "")

        script_dir = os.path.join(BASE_DIR, "gif_app", "scripts")

        generate_script = os.path.join(script_dir, "generate.py")
        gif_script = os.path.join(script_dir, "gif.py")
        edit_script = os.path.join(script_dir, "edit.py")

        # Ensure script exists before execution
        if not os.path.exists(generate_script):
            return HttpResponse("Error: generate.py not found", status=500)

        subprocess.run(["python", generate_script, text])

        # Ensure Blender executable path is correct
        blender_path = r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe"
        if not os.path.exists(blender_path):
            return HttpResponse("Error: Blender executable not found", status=500)

        blender_command = [blender_path, "-b", "--python", edit_script]
        subprocess.run(blender_command)

        subprocess.run(["python", gif_script])

        return HttpResponse("Success")

    return HttpResponse("Invalid Request", status=400)
