import json
import os
import yaml
import sys
import subprocess

input_client_id = sys.argv[1]
input_vpc_id = sys.argv[2]

current_directory = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_directory, '..', 'automation', 'variables', 'create_vpc_variables.yml')
json_file_path = os.path.join(current_directory, '..', 'database', 'database.json')

data = None
with open(json_file_path, 'r') as file:
    data = json.load(file)

for client, client_data in data.items():
    customer_id = client_data["customer_id"]
    if str(customer_id) == str(input_client_id):
        vpcs = client_data["vpcs"]
        for vpc_name, vpc_details in vpcs.items():
            vpc_id = vpc_details["vpc_id"]
            if str(vpc_id) == str(input_vpc_id):
                        v_id = f'c{customer_id}v{vpc_id}'
                        vpc_ip = vpc_details["vpc_ip"]
                        subnet_yaml_data = {
                            "pub_namespace": 'public',
                            "vpc_id": v_id,
                            "ep_in_pub": f've_{v_id}_pns',
                            "ep_in_vpc": f've_{v_id}_v',
                            "public_route_inf": 've_ns',
                            "pub_ns_ip": f'{vpc_ip}.1',
                            "pub_vpc_ep_ip": f'{vpc_ip}.1/30',
                            "vpc_ep_ip": f'{vpc_ip}.2/30',
                            "vpc_subnet": f'{vpc_ip}.0/30',
                        }
os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(subnet_yaml_data, yaml_file)

yaml_archive_file_path = os.path.join(current_directory, '../archive/automation/variables/create_vm_variables_'+str(v_id)+'.yml')
os.makedirs(os.path.dirname(yaml_archive_file_path), exist_ok=True)
with open(yaml_archive_file_path, 'w') as yaml_file:
    yaml.dump(subnet_yaml_data, yaml_file)

def run_ansible_playbook(playbook_path):
    try:
        subprocess.run(["sudo", "ansible-playbook", playbook_path], check=True)
        print("Ansible playbook executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Ansible playbook: {e}")
        return False

playbook_path = '../automation/ansible_create_vpc.yaml'
run_ansible_playbook(playbook_path)


