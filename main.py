from flask import Flask, render_template, jsonify, request,redirect,url_for
from function.retrive import get_all_data,get_data_by_node
from function.db_read import get_all_data_db



app = Flask(__name__,static_folder="static")



#Route
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')




#Data Retrive
@app.route('/api/data', methods=['GET'])
def get_data():
    node_id = request.args.get('node_id')  # Get node_id from request query parameter
    if node_id:  # If node_id is provided, filter data
        data = get_data_by_node(node_id)
    else:
        data = get_all_data()  # Otherwise, return all data
    return jsonify(data) 

@app.route('/api/data_db', methods=['GET'])
def fetch_data():
    data = get_all_data_db()
    
    # Convert to plain text format (CSV-like)
    response_text = "\n".join([f"{row['batch_no']},{row['start_time']},{row['end_time']},{row['date']},{row['set_qty']},{row['act_qty']},{row['destination']},{row['error']}" for row in data])
    
    return response_text, 200, {'Content-Type': 'text/plain'}




#Login

VALID_USERNAME = "Manav"
VALID_PASSWORD = "mvp@123"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '').strip()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error="Invalid username or password!")
    

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)