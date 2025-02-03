import subprocess
from flask import Flask, request, send_from_directory, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    text = request.form['text']
    subprocess.run(['python', 'generate.py', text])  
    
    blender_command = [
        r"C:\Program Files\Blender Foundation\Blender 4.3\blender.exe", 
        "-b", 
        "--python", r"edit.py"
    ]
    subprocess.run(blender_command) 

    subprocess.run(['python', 'gif.py'])  

    send_file('static/output.gif', as_attachment=True)
    
    return "Success"

@app.route('/edit', methods=['POST'])
def edit():
    text = request.form['text']
    subprocess.run(['python', 'generate.py', text]) 
    return "Success"

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=3000,debug=True)
