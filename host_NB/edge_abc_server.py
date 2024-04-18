from flask import Flask
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

@app.route('/')
def get_data():
    if not os.path.exists("data.txt"):     
        url = "http://1.1.1.2:1234/get_data"
        download_file(url, "data.txt")

    with open("data.txt", 'r') as file:
        content = file.read()

    return content

def download_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print("File downloaded successfully as", filename)
        else:
            print("Failed to download file. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

# Function to delete the file
def delete_file():
    file_path = "data.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"{file_path} deleted successfully")
    else:
        print(f"{file_path} does not exist")

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(delete_file, 'interval', seconds=60)  # Delete the file every hour
scheduler.start()

if __name__ == '__main__':
    # Run Flask app
    app.run(host="0.0.0.0", port=8080)


