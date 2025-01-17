from flask import Flask, request, redirect
import requests
import time
import ipaddress  # Use ipaddress module for IP comparison

app = Flask(__name__)

# Route to handle the redirect and logging of IP
@app.route('/')
def home():
    return redirect('/redirect')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Extract client IP
    client_ip = get_client_ip()

    # If the IP is private, return an error message
    if is_private_ip(client_ip):
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

    # After sending the IP, attempt to redirect the user to Google
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
            if not is_private_ip(ip):  # Ensure we only accept non-private IPs
                return ip
        return ip_list[-1]  # If all are private, use the last one (likely the proxy)
    else:
        # No X-Forwarded-For, fallback to remote address
        return request.remote_addr

# Function to check if the IP is a private IP using ipaddress module
def is_private_ip(ip):
    try:
        # Convert IP to ipaddress object
        ip_obj = ipaddress.ip_address(ip)
        # Check if the IP is private
        return ip_obj.is_private
    except ValueError:
        # If the IP format is invalid, treat it as private
        return True

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
