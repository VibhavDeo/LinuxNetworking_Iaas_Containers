from flask import Flask, request, jsonify
import json, random, requests

app = Flask(__name__)

def download_file(url, filename):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, 'w') as file:
                print(response)
                print(response.content)
                
                print(response.json())
                json.dump(response.json(), file, indent=4)
            print("File downloaded successfully as", filename)
        else:
            print("Failed to download file. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

# Route to handle client requests
@app.route("/", methods=["GET"])
def handle_request():
    url = "http://192.168.38.10:8000/get_dns_data"
    download_file(url, "dns_db.json")

    with open('countrymapping.json', 'r') as file:
        proximity = json.load(file)

    with open("dns_db.json", "r") as file:
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