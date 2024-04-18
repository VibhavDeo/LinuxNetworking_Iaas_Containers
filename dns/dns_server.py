from flask import Flask, request, jsonify
import json, random

app = Flask(__name__)

# Route to handle client requests
@app.route("/", methods=["GET"])
def handle_request():
    
    with open('../database/countrymapping.json', 'r') as file:
        proximity = json.load(file)

    with open("../database/dns_db.json", "r") as file:
        database = json.load(file)

    website = request.args.get("website")
    user_location = request.args.get("location")
    preferred_server = int(request.args.get("preferred_server"))

    server_location = proximity[user_location][preferred_server]
    if website in database:
        dst_list = []
        for loc in database[website]:
            if server_location.lower() in loc.lower():
                dst_list.append(database[website][loc])
        
        if dst_list:
            ip_address, port_number = random.choice(dst_list)
            print(ip_address)
            return jsonify({website: {server_location: (port_number, ip_address)}})
        else:
            return jsonify({"error": "No server found at the specified location"})

    else:
        return jsonify({"error": "No matching data found"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)