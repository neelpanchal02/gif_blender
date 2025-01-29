import subprocess
from flask import Flask, request, send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    subprocess.run(['python', 'generate.py', text])
    
    blender_command = [
        r"/home/tar/blender-4.3.2-linux-x64/blender",
        "-b", 
        "--python", r"edit.py"
    ]
    subprocess.run(blender_command) 

    subprocess.run(['python', 'gif.py'])  
    
    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
