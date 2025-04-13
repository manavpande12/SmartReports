import json
import os

class WriteJson:
    def __init__(self, file_path=os.path.join("log", "data.json")):  # ✅ Cross-platform path
        self.file_path = file_path
        self.ensure_file_exists()  # ✅ Ensures file exists on initialization

    def ensure_file_exists(self):
        """Creates an empty JSON file if it does not exist."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)  # ✅ Create 'log' directory if missing
            with open(self.file_path, "w") as file:
                json.dump([], file, indent=4)  # ✅ Initialize empty list

    def write_data(self, act_qty1, act_qty2, set_qty1,set_qty2, vessel1_active,vessel2_active,pause1,pause2):
        """Appends data to the JSON file instead of overwriting."""
        new_entry = {
            "act_qty1": act_qty1,
            "act_qty2": act_qty2,
            "set_qty1": set_qty1,
            "set_qty2": set_qty2,
            "vessel1": vessel1_active,
            "vessel2": vessel2_active,
            "pause1": pause1,
            "pause2": pause2,
        }

        # Load existing JSON data
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                if not isinstance(data, list):  # ✅ Ensure the JSON root is a list
                    data = []
        except (json.JSONDecodeError, FileNotFoundError):
            data = []  # ✅ Handle file missing or corrupt JSON case

        # Append new data and save
        data.append(new_entry)
        with open(self.file_path, "w") as file:
            json.dump(data, file, indent=4)

    def has_data(self):
        """Checks if JSON file contains any data."""
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
                return bool(data)  # ✅ Returns True if data exists
        except (json.JSONDecodeError, FileNotFoundError):
            return False

    def delete_content(self):
        """Deletes JSON content only if data exists."""
        if self.has_data():
            with open(self.file_path, "w") as file:
                json.dump([], file, indent=4)  # ✅ Reset JSON to empty list
