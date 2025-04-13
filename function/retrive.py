
import json
import os

json_file_path = os.path.join("log", "data.json")
# Function to fetch JSON data
def get_all_data():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        return data
    except json.JSONDecodeError as e:
        print(f"Loading JSON:{e}")
        return[]    

# Function to fetch data by node ID
def get_data_by_node(node_id):
    all_data = get_all_data()
    filtered_data = [entry for entry in all_data if entry.get("node_id") == node_id]
    return filtered_data

