# 📊 Smart Report Dashboard

## 📌 Overview

The **Smart Report Dashboard** is a real-time industrial data monitoring and reporting tool. It fetches data from an **OPC UA Server** (simulated using Prosys) and visualizes it using interactive charts on a web interface.

---

## 🚀 Features

- 🔌 **Real-time Data Fetching** from **OPC UA** using a Python service.
- 💾 **Dual Storage System**:
  - **JSON**: For real-time data visualization.
  - **PostgreSQL**: For storing historical records when a process is completed.
- 📉 **Stacked Bar Chart Visualization** with **Chart.js**, including:
  - Dynamic color changes based on machine state:
    - 🟢 **Running**
    - 🟡 **Paused**
    - 🔴 **Stopped**
  - Smooth animations and real-time updates.
- 📁 **Report Tab** for detailed insights and historical analysis.
- 🧠 **Smart Data Behavior**:
  - On **Start**: Data continuously stored in JSON and visualized live.
  - On **Pause**: JSON is cleared and only a "paused" state is logged.
  - On **Stop**: JSON is cleared and data is transferred to PostgreSQL.
- 📅 **Data Filters**:
  - Time-based: Last 24 hours, 7 days, 1 month, or all time.
  - Destination-based: **Vessel 1** or **Vessel 2**

---

## 🛠️ Tech Stack

- **Backend**: Python  
  - Flask (Web server)  
  - OPC UA (python-opcua)  
  - PyODBC  
  - Cryptography  
- **Database**: PostgreSQL (for persistent storage)
- **Frontend**: 
  - HTML, CSS, JavaScript  
  - **Chart.js** for real-time stacked bar graphs
- **Simulation**: Prosys OPC UA Simulation Server

---

## 🚀 Installation & Setup

### 1️⃣ Install Required Dependencies:
```bash
pip install Flask opcua pyodbc cryptography psycopg2
```

### 2️⃣ Create a Service Using NSSM (Windows)
NSSM (Non-Sucking Service Manager) is used to run the Python service in the background.


---

## 🔗 OPC UA Setup
- The **Prosys Simulation Software** is used as the OPC UA server.
- Update the **OPC UA URL** in the Python script to match the simulation server.

---

## 📷 Dashboard Preview
1. Login Screen
![image](https://github.com/user-attachments/assets/b31d999f-87a3-4392-ab60-db4bc640feb2)

2. Dashboard

Light Mode
![image](https://github.com/user-attachments/assets/2c53111e-1b73-4c33-a7d0-8ecd30541c41)

Dark Mode
![image](https://github.com/user-attachments/assets/3a4e721b-daf7-4b94-ac1b-861de9bcb5e0)


3. Reports

Light Mode
![image](https://github.com/user-attachments/assets/f3be3723-2ad3-4b7b-aea1-6f25df3cd185)


Dark Mode
![image](https://github.com/user-attachments/assets/a66aab1a-c9e9-4ab9-bb2e-905252c8e59d)



---

## 🤝 Contribution
Feel free to **fork** this repository and submit **pull requests** to improve the project.

---

## 📜 License
This project is licensed under the **MIT License**.

---

## 📧 Contact
For any queries, reach out via GitHub or email.

---

### ⭐ Don't forget to **star** this repository if you found it helpful!

