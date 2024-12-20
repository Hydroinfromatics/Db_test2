# Flask Sensor Data Application

This is a Flask-based web application for storing and retrieving sensor data. The application provides RESTful endpoints to submit sensor data and fetch stored records from a database.

## Features

- Submit sensor data through query parameters using the `/sensor-data` endpoint.
- Retrieve all stored sensor data with the `/sensor-data/all` endpoint.
- Validates input sensor data to ensure correctness and prevent invalid entries.

## Prerequisites

- Python 3.7 or higher.
- Flask installed.
- A MySQL or PostgreSQL database for storing sensor data.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install flask mysql-connector-python
   ```

3. **Database setup:**
   - Create a database (e.g., `sensor_data_db`).
   - Ensure the `sensor_data` table exists. The application will initialize it using the `create_table()` function.
   - Update the database connection details in the `connect_to_db` function.

## Usage

### Run the Application

Start the Flask server:
```bash
python TEST5.py
```
The application will run at `https://db-test2-4wp3.onrender.com`.

### Endpoints

#### **`GET /`**

Returns a message indicating the app is running.

#### **`GET /sensor-data`**

Adds or retrieves sensor data based on query parameters:

- **Add Data:** Include sensor parameters as query arguments. Example:
  ```bash
  curl "https://db-test2-4wp3.onrender.com/sensor-data?input_tds=100&output_tds=80&input_flow=50&output_flow=40&delivered_water=200&power=300&voltage=220&current=15"
  ```
- **Retrieve Data:** If no parameters are provided, it fetches all stored records:
  ```bash
  curl "https://db-test2-4wp3.onrender.com/sensor-data"
  ```

#### **`GET /sensor-data/all`**

Fetches all stored sensor data ordered by the `created_at` timestamp in descending order.

Example:
```bash
curl "https://db-test2-4wp3.onrender.com/sensor-data/all"
```

### Input Validation
The application validates the following parameters:

| Parameter       | Minimum Value | Maximum Value | Description               |
|-----------------|---------------|---------------|---------------------------|
| `input_tds`     | 1             | 10000         | Input Total Dissolved Solids |
| `output_tds`    | 1             | 10000         | Output Total Dissolved Solids|
| `input_flow`    | 0             | 100000        | Input water flow rate (L/h) |
| `output_flow`   | 0             | 100000        | Output water flow rate (L/h)|
| `delivered_water`| 0            | 100000        | Water delivered (L)       |
| `power`         | 0             | 10000         | Power consumption (W)     |
| `voltage`       | 0             | 500           | Voltage (V)               |
| `current`       | 0             | 1000          | Current (A)               |

### Database Schema

The `sensor_data` table structure:
```sql
CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    input_tds FLOAT NOT NULL,
    output_tds FLOAT NOT NULL,
    input_flow FLOAT NOT NULL,
    output_flow FLOAT NOT NULL,
    delivered_water FLOAT NOT NULL,
    power FLOAT NOT NULL,
    voltage FLOAT NOT NULL,
    current FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Error Handling

- **400 Bad Request:** Invalid input values.
- **500 Internal Server Error:** Issues with database connection or other server errors.

## Development

- **Debug Mode:** The app runs in debug mode for easier troubleshooting during development. Disable this in production by setting `debug=False` in `app.run()`.

## Contributing

Feel free to open issues or submit pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any queries, please contact [Gurudev] at [gurudev@iccwindia.org].

