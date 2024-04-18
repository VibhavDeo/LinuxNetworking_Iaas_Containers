from flask import Flask, jsonify, request
import json
import yaml
import requests
import random

app = Flask(__name__)

# Static customer and VM details
CUSTOMER_NAME = 'cdn3'
CUSTOMER_ID = 9
VM_MEMORY = "2048"
VM_VCPU = "2"
python_file_path='user_data/source.py'
optional_file_path='user_data/optional.txt'
file_path = 'user_data/random_numbers.txt'
# Mapping of edge servers to their VPC IDsn
edge_server_vpc_mapping = {
    'india': 'india',
    'usa': 'usa',
    'uk': 'uk'
}

# Mapping of edge servers to their interfaces
edge_server_interface_mapping = {
    'india': 've_c9v2_pns',
    'usa': 've_c9v3_pns',
    'uk': 've_c9v4_pns'
}

def generate_random_ip():
    """Generate a random IP address within the 192.168.0.0/16 subnet."""
    return f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.0"

def generate_unique_random_number(file_path):
    # Generate a random 3-digit number
    random_number = str(random.randint(100, 999))

    # Check if the random number already exists in the file
    with open(file_path, 'r') as file:
        existing_numbers = file.read().splitlines()

    while random_number in existing_numbers:
        random_number = str(random.randint(100, 999))

    # Append the random number to the file
    with open(file_path, 'a') as file:
        file.write(random_number + '\n')

    return random_number

# Example usage:


def create_and_upload_subnet_yaml(tenant_id, tenant_name, vpc_id, edge_server_responses,unique_random_number):
    """Generates and uploads subnet YAML file."""
    data = {
        'customer_name': CUSTOMER_NAME,
        'customer_id': CUSTOMER_ID,
        'vpcs': []
    }
    print(edge_server_responses)
    for edge_server in edge_server_responses:
        data['vpcs'].append({
            'vpc_name': edge_server['vpc_id'],
            'subnet_details': [{
                'subnet_name': f"{tenant_name}_{edge_server['name']}{unique_random_number}",
                'subnet_ip': generate_random_ip(),
                'subnet_mask': 24
            }]
        })

    with open('data.yaml', 'w') as yaml_file:
        yaml.dump(data, yaml_file, default_flow_style=False)

    return upload_yaml('data.yaml', 'http://1.1.1.1:8000/uploadSubnetDetails')

def create_and_upload_vm_yaml(edge_server_responses, tenant_name,unique_random_number):
    """Generates and uploads VM YAML file."""
    yaml_data = {
        'customer_name': CUSTOMER_NAME,
        'customer_id': CUSTOMER_ID,
        'vpcs': []
    }

    for edge_server in edge_server_responses:
        yaml_data['vpcs'].append({
            'vpc_name': edge_server['vpc_id'],
            'subnet_details': [{
                'subnet_name': f"{tenant_name}_{edge_server['name']}{unique_random_number}",
                'vm_details': [{'vm_name':f"{tenant_name}_{edge_server['name']}_vm", 'memory': VM_MEMORY, 'vcpu': VM_VCPU}],
            }]
        })

    with open('vm_details.yaml', 'w') as yaml_file:
        yaml.dump(yaml_data, yaml_file, default_flow_style=False)

    return upload_yaml_vm('vm_details.yaml', 'http://1.1.1.1:8000/uploadVMDetails')

def create_namespace_yaml(tenant_id, vpc_id, edge_server_responses):
    """Generates and uploads namespace YAML file."""
    namespace = "public"
    interface_pairs = []

    for edge_server in edge_server_responses:
        interface_pairs.append({
            'interface1': edge_server_interface_mapping[edge_server['name']],
            'interface2': f"ve_c{tenant_id}v{vpc_id}_pns"
        })

    namespace_data = {
        'namespace': namespace,
        'interface_pairs': interface_pairs
    }

    with open('namespace.yaml', 'w') as yaml_file:
        yaml.dump(namespace_data, yaml_file, default_flow_style=False)

    return upload_yaml('namespace.yaml', 'http://1.1.1.1:8000/uploadNamespaceDetails')

def upload_yaml(yaml_file_path, url):
    """Uploads the specified YAML file to the provided URL."""
    with open(yaml_file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()
            print(f"{yaml_file_path} successfully uploaded. Server response:")
            print(response.text)
            return True
        except requests.exceptions.RequestException as e:
            print(f"Failed to upload {yaml_file_path}: {e}")
            return False

def upload_yaml_vm(yaml_file_path, url):
    """Uploads the specified YAML file to the provided URL."""
    files = {}
    with open(yaml_file_path, 'rb') as file:
        files['file'] = file
        with open(python_file_path, 'rb') as file2:
            files['python_content'] = file2
            with open(optional_file_path, 'rb') as file3:
                files['data_content'] = file3
                try:
                    response = requests.post(url, files=files)
                    response.raise_for_status()
                    print(f"{yaml_file_path} successfully uploaded. Server response:")
                    print(response.text)
                    return True
                except requests.exceptions.RequestException as e:
                    print(f"Failed to upload {yaml_file_path}: {e}")
                    return False

@app.route('/init_gathering', methods=['POST'])
def init_data_gathering():
    unique_random_number=generate_unique_random_number(file_path)
    data = request.json
    tenant_id = data.get('tenant_id')
    tenant_name = data.get('tenant_name')
    vpc_id = data.get('vpc_id')


    edge_server_responses = []
    for edge_server, vpc in edge_server_vpc_mapping.items():
        include_server = data.get(f"include_{edge_server}")
        if include_server == 'yes':
            edge_server_responses.append({'name': edge_server, 'vpc_id': vpc})

    if tenant_id and tenant_name and vpc_id:
        if create_and_upload_subnet_yaml(tenant_id, tenant_name, vpc_id, edge_server_responses,unique_random_number):
            if create_and_upload_vm_yaml(edge_server_responses, tenant_name,unique_random_number):
                create_namespace_yaml(tenant_id, vpc_id, edge_server_responses)
        return jsonify({"message": "Data gathering and processing completed successfully"})
    else:
        return jsonify({"error": "Missing parameters"}), 400


@app.route('/get-data', methods=['GET'])
def get_data():
    """Endpoint to return the collected data."""
    with open('data.json') as json_file:
        data = json.load(json_file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='70.70.70.2', port=8080)