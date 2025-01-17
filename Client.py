from flask import Flask, request, redirect
import requests
from ipaddress import ip_address, ip_network

app = Flask(__name__)

# Define private IP ranges
private_ranges = [
    ip_network("10.0.0.0/8"),
    ip_network("172.16.0.0/12"),
    ip_network("192.168.0.0/16"),
    ip_network("127.0.0.0/8")  # Loopback address
]

# Function to check if the IP is private
def is_private_ip(ip):
    ip_obj = ip_address(ip)
    return any(ip_obj in net for net in private_ranges)

@app.route('/')
def home():
    # This will show a link to click
    return '<a href="/send_ip_and_redirect">Click to send your IP and go to Google</a>'

@app.route('/send_ip_and_redirect', methods=['GET'])
def send_ip_and_redirect():
    # Get the client's IP address
    client_ip = request.remote_addr  # Simple approach to get IP
    
    # If the IP is private, use X-Forwarded-For (if behind a proxy) or fallback
    if is_private_ip(client_ip):
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        if x_forwarded_for:
            # Get the first public IP in the X-Forwarded-For chain
            client_ip = x_forwarded_for.split(',')[0].strip()
    
    # If it's still a private IP, consider it invalid
    if is_private_ip(client_ip):
        return "Error: Could not determine a valid public IP address.", 400
    
    # Print the public IP for debugging
    print(f"Client Public IP: {client_ip}")

    # Send the IP to a target server
    target_server_url = "https://your-server-url.com/log_ip"  # Replace with your own server URL
    payload = {"ip": client_ip}

    try:
        # Send the IP to the target server
        response = requests.post(target_server_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending IP: {e}")

    # After sending the IP, redirect the user to Google
    return redirect('https://www.google.com')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
