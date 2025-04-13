from opcua import Client
from database.db_write import WriteDB
from datetime import datetime
import time
from jsonn.json_write import WriteJson

# PostgreSQL Connection Parameters
db_params = {
    "dbname": "Smart Report",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": "5432"
}

# OPC UA Server Connection
opcua_server_url = "opc.tcp:/OPCUA/SimulationServer"
nodes = {
    "pause1": "ns=3;i=1009",
    "pause2": "ns=3;i=1016",
    "vessel1": "ns=3;i=1010",
    "vessel2": "ns=3;i=1011",
    "set_qty1": "ns=3;i=1013",
    "set_qty2": "ns=3;i=1015",
    "act_qty1": "ns=3;i=1014",
    "act_qty2": "ns=3;i=1012"
}

# Connect to OPC UA Server
client = Client(opcua_server_url)
client.connect()
print("✅ OPC UA Client Connected")

# Initialize Database Handler
db = WriteDB(db_params)
db.create_table()

# Initialize JSON Handler
js = WriteJson()

# Tracking variables
vessel1_active = False
vessel2_active = False
start_time = None
destination = ""
set_qty = 0
act_qty = 0
last_json_update = time.time()  # Track last JSON update

try:
    while True:
        # Read values from OPC UA
        pause1 = client.get_node(nodes["pause1"]).get_value()
        pause2 = client.get_node(nodes["pause2"]).get_value()
        vessel1_state = client.get_node(nodes["vessel1"]).get_value()
        vessel2_state = client.get_node(nodes["vessel2"]).get_value()
        set_qty1 = client.get_node(nodes["set_qty1"]).get_value()
        set_qty2 = client.get_node(nodes["set_qty2"]).get_value()
        act_qty1 = client.get_node(nodes["act_qty1"]).get_value()
        act_qty2 = client.get_node(nodes["act_qty2"]).get_value()

        # ✅ If Vessel 1 starts, record the start time and set destination
        if vessel1_state and not vessel1_active:
            start_time = datetime.now().strftime("%H:%M:%S")
            destination = "Vessel 1"
            set_qty = set_qty1
            act_qty = act_qty1
            vessel1_active = True
            print(f"🚀 Vessel 1 Started at {start_time}, Destination: {destination}")

        # ✅ If Vessel 2 starts, record the start time and set destination
        if vessel2_state and not vessel2_active:
            start_time = datetime.now().strftime("%H:%M:%S")
            destination = "Vessel 2"
            set_qty = set_qty2
            act_qty = act_qty2
            vessel2_active = True
            print(f"🚀 Vessel 2 Started at {start_time}, Destination: {destination}")

        # ✅ If pause1 is True, wait for it to turn False before proceeding
        if vessel1_active and pause1:
            print("⏸️ Vessel 1 Paused, Waiting...")
            if js.has_data():
                js.delete_content()
                print("🗑️ Deleted all content from log/data.json. becasue pause 1 is True")
            js.write_data(act_qty1, act_qty2, set_qty1, set_qty2, vessel1_active, vessel2_active,pause1,pause2)
            while client.get_node(nodes["pause1"]).get_value():
                if not client.get_node(nodes["vessel1"]).get_value():  # Vessel 1 stops while paused
                    break
                time.sleep(1)

        # ✅ If pause2 is True, wait for it to turn False before proceeding
        if vessel2_active and pause2:
            print("⏸️ Vessel 2 Paused, Waiting...")
            if js.has_data():
                js.delete_content()
                print("🗑️ Deleted all content from log/data.json. becasue pause 2 is True")
            js.write_data(act_qty1, act_qty2, set_qty1, set_qty2, vessel1_active, vessel2_active,pause1,pause2)
            while client.get_node(nodes["pause2"]).get_value():
                if not client.get_node(nodes["vessel2"]).get_value():  # Vessel 2 stops while paused
                    break
                time.sleep(1)

        # ✅ JSON update every 10 seconds when a vessel is active
        current_time = time.time()
        if (vessel1_active or vessel2_active) and (current_time - last_json_update >= 1) and (not pause1 or not pause2):
            js.write_data(act_qty1, act_qty2, set_qty1, set_qty2, vessel1_active, vessel2_active,pause1,pause2)
            last_json_update = current_time
            print("✅ JSON Updated Every 10 Seconds")

        
            


        # ✅ If Vessel 1 stops (including when paused), store data and clear JSON
        if (not vessel1_state and vessel1_active) or (vessel1_active and pause1 and not vessel1_state):
            end_time = datetime.now().strftime("%H:%M:%S")
            print(f"🔴 Vessel 1 Stopped at {end_time}, Final Act Qty: {act_qty}")
            db.insert_data(start_time, end_time, datetime.now().strftime("%Y-%m-%d"), set_qty, act_qty, destination)

            # ✅ Clear JSON if data exists
            if js.has_data():
                js.delete_content()
                print("🗑️ Deleted all content from log/data.json as Vessel 1 is OFF.")

            # Reset all states
            vessel1_active = False
            start_time = None
            destination = ""
            set_qty = 0
            act_qty = 0

        # ✅ If Vessel 2 stops (including when paused), store data and clear JSON
        if (not vessel2_state and vessel2_active) or (vessel2_active and pause2 and not vessel2_state):
            end_time = datetime.now().strftime("%H:%M:%S")
            print(f"🔴 Vessel 2 Stopped at {end_time}, Final Act Qty: {act_qty}")
            db.insert_data(start_time, end_time, datetime.now().strftime("%Y-%m-%d"), set_qty, act_qty, destination)

            # ✅ Clear JSON if data exists
            if js.has_data():
                js.delete_content()
                print("🗑️ Deleted all content from log/data.json as Vessel 2 is OFF.")

            # Reset all states
            vessel2_active = False
            start_time = None
            destination = ""
            set_qty = 0
            act_qty = 0

        time.sleep(1)  # Poll every second

except KeyboardInterrupt:
    print("⛔ Process stopped manually")
finally:
    client.disconnect()
    print("✅ OPC UA Client Disconnected")
