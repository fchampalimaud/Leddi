import json

# Function to load JSON data
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to load JSON data as a string
def load_json_to_str(file_path):
    with open(file_path, 'r') as file:
        return json.dumps(json.load(file))

# Function to save JSON data
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)