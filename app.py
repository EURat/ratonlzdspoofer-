import threading
import webview
from flask import Flask, jsonify, request, render_template
import random
import string
import logging
import subprocess
import psutil

app = Flask(__name__)

# Setup logging
logging.basicConfig(filename='hardware_id_changes.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# Store original hardware IDs on app start
original_cpu_ids = []
original_hd_serials = []

current_cpu_ids = []
current_hd_serials = []

def run_wmic_command(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        lines = result.strip().splitlines()
        # Remove header line if present
        if len(lines) > 1:
            return [line.strip() for line in lines[1:] if line.strip()]
        else:
            return []
    except Exception as e:
        logging.error(f"Error running WMIC command '{command}': {e}")
        return []

def get_all_cpu_ids():
    # Try WMIC command to get ProcessorId
    cpu_ids = run_wmic_command("wmic cpu get ProcessorId")
    if cpu_ids:
        return cpu_ids
    else:
        return ["Unknown"]

def get_all_hd_serials():
    # Try WMIC command to get DiskDrive serial numbers
    hd_serials = run_wmic_command("wmic diskdrive get SerialNumber")
    if hd_serials:
        return hd_serials
    else:
        return ["Unknown"]

def random_string(length=16):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def initialize_ids():
    global original_cpu_ids, original_hd_serials, current_cpu_ids, current_hd_serials
    original_cpu_ids = get_all_cpu_ids()
    original_hd_serials = get_all_hd_serials()
    current_cpu_ids = original_cpu_ids.copy()
    current_hd_serials = original_hd_serials.copy()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_ids', methods=['GET'])
def api_get_ids():
    return jsonify({
        'cpu_ids': current_cpu_ids,
        'hd_serials': current_hd_serials
    })

@app.route('/api/randomize', methods=['POST'])
def api_randomize():
    global current_cpu_ids, current_hd_serials
    new_cpu_ids = [random_string(16) for _ in current_cpu_ids]
    new_hd_serials = [random_string(16) for _ in current_hd_serials]

    logging.info(f"Randomized CPU IDs from {current_cpu_ids} to {new_cpu_ids}")
    logging.info(f"Randomized Hard Drive Serial Numbers from {current_hd_serials} to {new_hd_serials}")

    current_cpu_ids = new_cpu_ids
    current_hd_serials = new_hd_serials

    return jsonify({
        'cpu_ids': current_cpu_ids,
        'hd_serials': current_hd_serials,
        'message': 'Hardware IDs randomized (simulated).'
    })

@app.route('/api/revert', methods=['POST'])
def api_revert():
    global current_cpu_ids, current_hd_serials
    current_cpu_ids = original_cpu_ids.copy()
    current_hd_serials = original_hd_serials.copy()

    logging.info(f"Reverted CPU IDs to original: {original_cpu_ids}")
    logging.info(f"Reverted Hard Drive Serial Numbers to original: {original_hd_serials}")

    return jsonify({
        'cpu_ids': current_cpu_ids,
        'hd_serials': current_hd_serials,
        'message': 'Hardware IDs reverted to original.'
    })

@app.route('/api/processes', methods=['GET'])
def api_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            processes.append({'pid': proc.info['pid'], 'name': proc.info['name']})
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return jsonify(processes)

@app.route('/api/kill_process', methods=['POST'])
def api_kill_process():
    data = request.get_json()
    pid = data.get('pid')
    if pid is None:
        return jsonify({'success': False, 'message': 'No PID provided'}), 400
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait(timeout=3)
        logging.info(f"Killed process {pid} ({proc.name()})")
        return jsonify({'success': True, 'message': f'Process {pid} killed successfully'})
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as e:
        logging.error(f"Failed to kill process {pid}: {e}")
        return jsonify({'success': False, 'message': f'Failed to kill process {pid}: {e}'}), 500

def start_flask():
    initialize_ids()
    app.run()

if __name__ == '__main__':
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Open native window with pywebview pointing to Flask app
    webview.create_window("Hardware ID Shower", "http://127.0.0.1:5000", width=900, height=600)
    webview.start()
