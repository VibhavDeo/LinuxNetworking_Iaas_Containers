import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_data():
    return "Hello world from XYZ"
# Set the current working directory to the directory of the Python script
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

@app.route('/get_data')
def send_file_data():
    with open('data.txt', 'r') as file:
        file_content = file.read()
    return file_content

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

