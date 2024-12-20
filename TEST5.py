from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta

app = Flask(__name__)

# Database configuration
db_config = {
    "host": "hip-mysql-iccw-hip.j.aivencloud.com",
    "user": "avnadmin",
    "password": "AVNS_aPCpCSKO_x8aBGEKcNq",
    "database": "defaultdb",
    "port": 25381,
    "ssl_ca": r"D:\mysql\gurudev_new\ca.pem"  # Path to your CA certificate
}

# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connection to MySQL database was successful!")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Function to create sensor data table
def create_table():
    try:
        connection = connect_to_db()
        if connection:
            cursor = connection.cursor()
            create_sensor_table_query = """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_tds FLOAT NOT NULL CHECK (input_tds >= 1 AND input_tds <= 10000),
                output_tds FLOAT NOT NULL CHECK (output_tds >= 1 AND output_tds <= 10000),
                input_flow FLOAT NOT NULL CHECK (input_flow >= 0 AND input_flow <= 100000),
                output_flow FLOAT NOT NULL CHECK (output_flow >= 0 AND output_flow <= 100000),
                delivered_water FLOAT NOT NULL CHECK (delivered_water >= 0 AND delivered_water <= 100000),
                power FLOAT NOT NULL CHECK (power >= 0 AND power <= 10000),
                voltage FLOAT NOT NULL CHECK (voltage >= 0 AND voltage <= 500),
                current FLOAT NOT NULL CHECK (current >= 0 AND current <= 1000),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(create_sensor_table_query)
            connection.commit()
            print("Table 'sensor_data' is ready.")
    except Error as e:
        print(f"Error while creating table: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

@app.route('/')
def home():
    return "Flask app is running! Use /sensor-data endpoint to submit or retrieve data."

def validate_sensor_input(data, key, min_value=None, max_value=None, param_name=None):
    value = data.get(key)
    param_name = param_name or key
    try:
        value = float(value)
        if min_value is not None and value < min_value:
            raise ValueError(f"{param_name} must be >= {min_value}.")
        if max_value is not None and value > max_value:
            raise ValueError(f"{param_name} must be <= {max_value}.")
        return value
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid value for {param_name}: {e}")

@app.route('/sensor-data', methods=['GET'])
def handle_sensor_data():
    # Check if any sensor parameters are provided
    if any(param in request.args for param in ['input_tds', 'output_tds', 'input_flow', 'output_flow', 
                                             'delivered_water', 'power', 'voltage', 'current']):
        return add_sensor_data()
    else:
        return get_all_sensor_data()

def add_sensor_data():

    conn = None
    cursor = None
    try:
        # Validate all sensor inputs from query parameters
        input_tds = validate_sensor_input(request.args, 'input_tds', min_value=1, max_value=10000, param_name="Input TDS")
        output_tds = validate_sensor_input(request.args, 'output_tds', min_value=1, max_value=10000, param_name="Output TDS")
        input_flow = validate_sensor_input(request.args, 'input_flow', min_value=0, max_value=100000, param_name="Input Flow")
        output_flow = validate_sensor_input(request.args, 'output_flow', min_value=0, max_value=100000, param_name="Output Flow")
        delivered_water = validate_sensor_input(request.args, 'delivered_water', min_value=0, max_value=100000, param_name="Delivered Water")
        power = validate_sensor_input(request.args, 'power', min_value=0, max_value=10000, param_name="Power")
        voltage = validate_sensor_input(request.args, 'voltage', min_value=0, max_value=500, param_name="Voltage")
        current = validate_sensor_input(request.args, 'current', min_value=0, max_value=1000, param_name="Current")

        conn = connect_to_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        sql = """INSERT INTO sensor_data 
                (input_tds, output_tds, input_flow, output_flow, delivered_water, power, voltage, current)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (input_tds, output_tds, input_flow, output_flow, delivered_water, power, voltage, current)
        
        cursor.execute(sql, values)
        conn.commit()
        
        return jsonify({
            "message": "Sensor data stored successfully",
            "id": cursor.lastrowid,
            "data": {
                "input_tds": input_tds,
                "output_tds": output_tds,
                "input_flow": input_flow,
                "output_flow": output_flow,
                "delivered_water": delivered_water,
                "power": power,
                "voltage": voltage,
                "current": current
            }
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
# Route to fetch weekly records
@app.route('/sensor-data/all', methods=['GET'])
def get_all_sensor_data():
    conn = None
    cursor = None
    try:
        conn = connect_to_db()
        if not conn:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM sensor_data ORDER BY created_at DESC")
        records = cursor.fetchall()
        
        # Convert datetime objects to strings for JSON serialization
        for record in records:
            record['created_at'] = record['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

# Initialize the database table
create_table()

if __name__ == '__main__':
    app.run(debug=True)