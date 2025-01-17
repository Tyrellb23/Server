import os
from flask import Flask, request, redirect
import ipaddress

app = Flask(__name__)

# Helper function to determine if an IP is private
def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private
    except ValueError:
        return True  # If the IP format is invalid, treat it as private

# Helper function to extract the real client IP from headers (supporting proxies)
def get_client_ip():
    # Check for 'X-Forwarded-For' header which may contain multiple IP addresses
    x_forwarded_for = request.headers.get('X-Forwarded-For')

    # If 'X-Forwarded-For' exists, it may contain a list of IPs
    if x_forwarded_for:
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        
        # Iterate through each IP in the list to find the first non-private IP
        for ip in ip_list:
            if not is_private_ip(ip):
                print(f"Using public IP: {ip}")
                return ip
        
        # If all IPs are private, return the last one (which might be the proxy's IP)
        # This ensures that we don’t fallback to the remote address unless necessary
        print(f"All IPs in X-Forwarded-For are private. Returning the last IP: {ip_list[-1]}")
        return ip_list[-1]
    
    # If no 'X-Forwarded-For' header is present, return a message or use the fallback
    # For this case, we won't fall back to `request.remote_addr` unless absolutely needed.
    print("No X-Forwarded-For header found. Unable to determine public IP.")
    return None

@app.route('/log_ip', methods=['POST'])
def log_ip():
    try:
        # Extract the IP address from the POST request payload
        data = request.get_json()
        client_ip = data.get("ip")

        if client_ip:
            # Log the IP address to the console
            print(f"Received IP Address: {client_ip}")

            # Optionally save the IP address to a file
            with open("received_ips.txt", "a") as file:
                file.write(f"{client_ip}\n")

            return {"status": "success", "message": "IP logged successfully"}, 200
        else:
            return {"status": "error", "message": "No IP provided"}, 400
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.route('/')
def home():
    # Extract the real public IP address before redirecting
    client_ip = get_client_ip()
    
    if client_ip:
        print(f"Client Public IP: {client_ip}")
    else:
        print("Unable to determine client public IP.")

    # Now redirect the user to Google
    return redirect("https://www.google.com")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
