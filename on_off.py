from flask import Flask, render_template_string
import serial
import threading

# Initialize Flask app
app = Flask(__name__)

# Initialize Serial Communication with Arduino
try:
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=5)
    print("Serial connection initialized successfully.")
except serial.SerialException as e:
    print(f"Error: Could not open serial port: {e}")
    ser = None

# Function to continuously read from Serial and print to console
def read_from_serial():
    if ser:
        while True:
            try:
                if ser.in_waiting > 0:  # Check if data is available
                    line = ser.readline().decode('utf-8').strip()  # Read and decode a line
                    if line:
                        print(f"Arduino Output: {line}")
            except Exception as e:
                print(f"Error reading from serial: {e}")
                break

# Start a separate thread to monitor the serial output
if ser:
    serial_thread = threading.Thread(target=read_from_serial, daemon=True)
    serial_thread.start()

@app.route('/')
def home():
    # HTML for ON/OFF toggle, movement buttons, and mode switches
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Arduino Control</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                background: linear-gradient(to right, #ff7e5f, #feb47b);
                color: white;
            }
            .toggle-button {
                position: relative;
                display: inline-block;
                width: 100px;
                height: 50px;
                margin: 20px;
            }
            .toggle-button input {
                display: none;
            }
            .slider {
                position: absolute;
                cursor: pointer;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: #ccc;
                transition: 0.4s;
                border-radius: 25px;
            }
            .slider:before {
                position: absolute;
                content: "";
                height: 42px;
                width: 42px;
                left: 4px;
                bottom: 4px;
                background-color: white;
                transition: 0.4s;
                border-radius: 50%;
            }
            input:checked + .slider {
                background-color: #4CAF50;
            }
            input:checked + .slider:before {
                transform: translateX(50px);
            }
            .button {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 20px;
                cursor: pointer;
                border-radius: 8px;
                transition: background-color 0.3s;
            }
            .button:hover {
                background-color: #45a049;
            }
        </style>
        <script>
            function toggleDevice(checkbox) {
                const url = checkbox.checked ? "/on" : "/off";
                fetch(url)
                    .then(response => response.text())
                    .then(data => console.log(data))
                    .catch(error => console.error("Error:", error));
            }

            function sendCommand(command) {
                fetch(`/${command}`)
                    .then(response => response.text())
                    .then(data => console.log(data))
                    .catch(error => console.error("Error:", error));
            }
        </script>
    </head>
    <body>
        <h1>Arduino Control Panel</h1>
        <label class="toggle-button">
            <input type="checkbox" onchange="toggleDevice(this)">
            <span class="slider"></span>
        </label>
        <p>Toggle to turn Arduino ON/OFF</p>

        <button class="button" onclick="sendCommand('user')">USER Mode</button>
        <button class="button" onclick="sendCommand('auto')">AUTO Mode</button>

        <button class="button" onclick="sendCommand('forward')">FORWARD</button>
        <button class="button" onclick="sendCommand('backward')">BACKWARD</button>
        <button class="button" onclick="sendCommand('left')">LEFT</button>
        <button class="button" onclick="sendCommand('right')">RIGHT</button>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/on')
def turn_on():
    try:
        if ser and ser.is_open:
            ser.write(b'ON\n')
            return "Arduino Turned ON"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending ON command: {e}", 500

@app.route('/off')
def turn_off():
    try:
        if ser and ser.is_open:
            ser.write(b'OFF\n')
            return "Arduino Turned OFF"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending OFF command: {e}", 500

@app.route('/user')
def switch_to_user():
    try:
        if ser and ser.is_open:
            ser.write(b'USER\n')
            return "Switched to USER Mode"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending USER command: {e}", 500

@app.route('/auto')
def switch_to_auto():
    try:
        if ser and ser.is_open:
            ser.write(b'AUTO\n')
            return "Switched to AUTO Mode"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending AUTO command: {e}", 500

@app.route('/forward')
def move_forward():
    try:
        if ser and ser.is_open:
            ser.write(b'FORWARD\n')
            return "Moving FORWARD"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending FORWARD command: {e}", 500

@app.route('/backward')
def move_backward():
    try:
        if ser and ser.is_open:
            ser.write(b'BACKWARD\n')
            return "Moving BACKWARD"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending BACKWARD command: {e}", 500

@app.route('/left')
def move_left():
    try:
        if ser and ser.is_open:
            ser.write(b'LEFT\n')
            return "Turning LEFT"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending LEFT command: {e}", 500

@app.route('/right')
def move_right():
    try:
        if ser and ser.is_open:
            ser.write(b'RIGHT\n')
            return "Turning RIGHT"
        else:
            return "Serial connection not available", 500
    except Exception as e:
        return f"Error sending RIGHT command: {e}", 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8003, debug=True)
