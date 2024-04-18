import json
import os
import yaml
import sys
import subprocess


input_client_id = sys.argv[1]
input_vpc_id = sys.argv[2]
input_subnet_id = sys.argv[3]
input_vm_id = sys.argv[4]
print(input_client_id, input_vpc_id, input_subnet_id, input_vm_id)

current_directory = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_directory, '..', 'automation', 'variables', 'create_vm_variables.yml')
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
                subnet_details = vpc_details["subnet_details"]
                for subnet_name, subnet_info in subnet_details.items():
                    subnet_id = subnet_info["subnet_id"]
                    if str(subnet_id) == str(input_subnet_id):
                        vm_details = subnet_info["vm_details"]
                        for vm_name, vm_details in vm_details.items():
                            vm_id = vm_details["vm_id"]
                            if str(vm_id) == str(input_vm_id):
                                subnet_ip = subnet_info["subnet_ip"]
                                subnet_mask = str(subnet_info["subnet_mask"])
                                port = subnet_info["incoming_dnat_routing_port"]
                                v_id = f'c{customer_id}v{vpc_id}'
                                sn_id = f'{v_id}s{subnet_id}'
                                network_id = f'n{sn_id}'
                                vm_ip = '.'.join(subnet_ip.split('.')[:-1]) + '.'+str(vm_id)+'/' + subnet_mask
                                vm_ip_nmsk = '.'.join(subnet_ip.split('.')[:-1]) + '.'+str(vm_id)
                                subnet_ip = '.'.join(subnet_ip.split('.')[:-1]) + '.1'
                                vm_id = f'vm{vm_id}{sn_id}'
                                vpc_ip = vpc_details["vpc_ip"]
                                memory = vm_details["memory"]
                                vcpu = vm_details["vcpu"]
                                subnet_yaml_data = {
                                    "vm_port": 8080,
                                    "pub_namespace": "public",
                                    "template_dir": "/home/vmadm/project/automation/jinja_templates",
                                    "script_files_dir": "/home/vmadm/project/subnet_files",
                                    "public_router_ip": "1.1.1.2",
                                    "interface_name": "enp1s0",
                                    "vpc_id": v_id,
                                    "network_id": network_id,
                                    "vpc_incoming_port": port,
                                    "public_router_incoming_port": port,
                                    "veth_vpns_v_inf": f'{vpc_ip}.2',
                                    "subnet_ip": subnet_ip,
                                    "vm_ip": vm_ip,
                                    "vm_ip_nmsk": vm_ip_nmsk,
                                    "vm_id": vm_id,
                                    "memory": memory,
                                    "vcpu": vcpu
                                }

os.makedirs(os.path.dirname(yaml_file_path), exist_ok=True)
with open(yaml_file_path, 'w') as yaml_file:
    yaml.dump(subnet_yaml_data, yaml_file)

yaml_archive_file_path = os.path.join(current_directory, '../archive/automation/variables/create_vm_variables_'+f'vm{vm_id}{sn_id}'+'.yml')
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

playbook_path = '../automation/ansible_create_vm.yaml'
run_ansible_playbook(playbook_path)