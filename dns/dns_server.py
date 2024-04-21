from flask import Flask, request, jsonify
import json, random, requests
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=["GET"])
def handle_request():
    # Load country mapping and DNS database
    with open('../database/countrymapping.json', 'r') as file:
        proximity = json.load(file)

    with open("../database/dns_db.json", "r") as file:
        database = json.load(file)

    # Extract parameters from the request
    website = request.args.get("website")
    user_location = request.args.get("location")
    preferred_server = int(request.args.get("preferred_server"))

    # Get server location based on user location and preferred server
    server_location = proximity[user_location][preferred_server]

    # Log request information with timestamp
    log = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "website": website,
        "user_location": user_location,
        "preferred_server": preferred_server,
        "server_location": server_location
    }

    # Load existing logs from request_logs.json
    try:
        with open("request_logs.json", "r") as log_file:
            logs = json.load(log_file)
    except FileNotFoundError:
        logs = []

    # Add current log to the list of logs
    logs.append(log)

    # Store the logs in request_logs.json
    with open("request_logs.json", "w") as log_file:
        json.dump(logs, log_file, indent=4)

    # Check if the website exists in the database
    if website in database:
        dst_list = []
        for loc in database[website]:
            if server_location.lower() in loc.lower():
                dst_list.append(database[website][loc])
        
        if dst_list:
            ip_address, port_number = random.choice(dst_list)
            return jsonify({website: {server_location: (port_number, ip_address)}})
        else:
            return jsonify({"error": "No server found at the specified location"})

    else:
        return jsonify({"error": "No matching data found"})

if __name__ == "__main__":
    app.run()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)