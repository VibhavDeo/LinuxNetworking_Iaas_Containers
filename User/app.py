import requests
from requests.exceptions import Timeout

def get_ip_port(website, location,preferred_server):
    url = f"http://192.168.38.10:8080?website={website}&location={location}&preferred_server={preferred_server}"
    response = requests.get(url)
    data = response.json()
    website_data = data.get(website)
    if website_data:
        server_location = list(website_data.keys())[0]
        return data[website][server_location]
    else:
        return None

def make_second_request(ip_address, port_number):
    url = f"http://{ip_address}:{port_number}"
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except Timeout:
        return None

website = input("Enter website: ")
location = input("Enter your country: ")
i = 0

while i<3:
    ip_port = get_ip_port(website, location, i)
    if ip_port:
        ip_address, port_number = ip_port
        second_request_response = make_second_request(ip_address, port_number)
        if second_request_response:
            print('\n' + str(second_request_response) + '\n')
            break
        else:
            print("Failed to make request to the server")
    else:
        i += 1
