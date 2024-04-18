import json
from ruamel.yaml import YAML
import random
import os

current_directory = os.path.dirname(os.path.abspath(__file__))

yaml_file_path = os.path.join(current_directory, '..', 'automation', 'create_vpc_variables2.yml')
og_yaml_file_path = os.path.join(current_directory, '..', 'automation', 'ansible_create_vpc.yaml')
json_file_path = os.path.join(current_directory, '..', 'database', 'vpc_data.json')

with open(og_yaml_file_path, 'r') as file:
    existing_yaml_content = file.read()


# Function to generate random prefix
def generate_random_prefix(used_prefixes):
    prefix = ".".join([str(random.randint(0, 255)) for _ in range(3)])
    while prefix in used_prefixes:
        prefix = ".".join([str(random.randint(0, 255)) for _ in range(3)])
    return prefix

# Load JSON data from file
with open(json_file_path) as f:
    data = json.load(f)
print("The printed data is: "+ str(data))
# Load used prefixes from file or initialize an empty list
try:
    with open('used_prefixes.txt', 'r') as prefix_file:
        used_prefixes = prefix_file.read().splitlines()
except FileNotFoundError:
    used_prefixes = []

# Initialize a list to hold the transformed data
vpc_details = []
def customer_no():
    # Define a global variable to store the integer value
    global customer_counter
    
    # Initialize the counter if it doesn't exist
    if 'customer_counter' not in globals():
        customer_counter = 1
    
    # Increment the counter
    customer_counter += 1
    
    # Return the incremented value
    return customer_counter

def vpc_no():
    # Define a global variable to store the integer value
    global vpc_counter
    
    # Initialize the counter if it doesn't exist
    if 'vpc_counter' not in globals():
        vpc_counter = 1
    
    # Increment the counter
    vpc_counter += 1
    
    # Return the incremented value
    return vpc_counter



# Process each customer's details
for customer, info in data.items():
    print("the customer is: " + str(customer))
    details = []
    for detail in info['details']:
        prefix = generate_random_prefix(used_prefixes)
        vpc_id = f"c{customer_no()}v{vpc_no()}"
        details.append({
            'vpc_id': vpc_id,#CXVX
            'ep_in_pub': f"ve_{vpc_id}_pns",
            'ep_in_vpc': f"ve_{vpc_id}_v",
            'pub_ns_ip': "10.10.10.1",#10.10.1x.x
            'pub_vpc_ep_ip': f"{prefix}.1/30",
            'vpc_ep_ip': f"{prefix}.1/30",
            'vpc_subnet': f"{prefix}.1/30",
            'public_route_inf': "ve_ns", 
        })
        used_prefixes.append(prefix)
    vpc_details.append({'name': info['name'], 'vpcs': details})

# Write the YAML data to a file with proper indentation using ruamel.yaml
yaml = YAML()
data_og = yaml.load(existing_yaml_content)
data_og['vpc_details'] = str(vpc_details)

yaml.indent(mapping=2, sequence=4, offset=2)
# with open(yaml_file_path, 'w') as f:
#     yaml.dump({'vpc_details': vpc_details}, f)
with open(yaml_file_path, 'w') as file:
    yaml.dump(data_og, file)