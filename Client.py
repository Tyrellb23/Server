from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/redirect')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    try:
        # Extract client IP
        client_ip = get_client_ip()

        # Print the client IP for debugging
        print(f"Client IP: {client_ip}")

        # Send the IP address to another server
        target_server_url = "https://your-heroku-app.herokuapp.com/log_ip"  # Ensure this is correct
        payload = {"ip": client_ip}

        # POST request to log IP
        response = requests.post(target_server_url, json=payload)
        print(f"Response from log_ip: {response.status_code}")

        # Conditional redirect based on IP
        if client_ip.startswith("192.168"):
            target_url = "https://example.com"
        else:
            target_url = "https://google.com"

        print(f"Redirecting to {target_url}")
        return redirect(target_url)
    
    except Exception as e:
        print(f"Error during redirect: {e}")
        return f"An error occurred during the redirection process: {e}", 500

def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ip_list:
            if not is_private_ip(ip):
                return ip
        else:
            return ip_list[-1]
    else:
        return request.remote_addr

def is_private_ip(ip):
    private_ip_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255"),
        ("127.0.0.0", "127.255.255.255")
    ]
    
    ip_int = int(ip.replace('.', ''))
    for start, end in private_ip_ranges:
        start_int = int(start.replace('.', ''))
        end_int = int(end.replace('.', ''))
        if start_int <= ip_int <= end_int:
            return True
    return False

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

