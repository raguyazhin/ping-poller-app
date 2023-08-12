from flask import Flask, request, jsonify
import ipaddress
import subprocess
import concurrent.futures
import socket

app = Flask(__name__)

hostName = socket.gethostname()

def ping_ip(ip):

    try:
        status = subprocess.call(['ping', '-c', '5', str(ip)],)
        if status == 0:
            return "1"
        else:
            return "0"
    except subprocess.CalledProcessError as e:
        return "0"

@app.route('/ping', methods=['GET', 'POST'])
def ping_endpoint():
    try:
        if request.method == 'GET':
            ip_addresses_str = request.args.get('ip_addresses', default='', type=str)
            ip_addresses = ip_addresses_str.split(',')
        elif request.method == 'POST':
            data = request.json
            ip_addresses = data.get('ip_addresses', [])

        output_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ping_ip, ip_addresses)

        for ip_str, result in zip(ip_addresses, results):
            output_data.append({
                "ip": ip_str,
                "ping_success": result,
                "polling_host" : hostName
            })

        return jsonify({"ping_results": output_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
