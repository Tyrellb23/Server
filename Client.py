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

# Helper function to extract the real client IP
def get_client_ip():
    x_forwarded_for = request.headers.get('X-Forwarded-For')
    
    if x_forwarded_for:
        # X-Forwarded-For can contain a list of IPs, so we get the first one
        ip_list = [ip.strip() for ip in x_forwarded_for.split(',')]
        for ip in ip_list:
            # Check if it's not a private IP
            if not is_private_ip(ip):
                return ip
        # If all are private IPs, return None (indicating no valid public IP was found)
        return None
    else:
        # If no X-Forwarded-For header, return None for now
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
    max_attempts = 5  # Maximum number of retry attempts
    delay = 2  # Delay in seconds between retries
    
    for attempt in range(max_attempts):
        # Log the real public IP address before doing the redirect
        client_ip = get_client_ip()
        
        if client_ip:
            print(f"Found Public IP: {client_ip}")
            # Now redirect the user to Google
            return redirect("https://www.google.com")
        
        # If no valid public IP was found, retry after the delay
        print(f"Attempt {attempt + 1}: No valid public IP found. Retrying...")
        
        if attempt < max_attempts - 1:
            time.sleep(delay)  # Wait before retrying
    
    # If no valid public IP found after retries, return an error
    return "Error: Could not determine a valid public IP address.", 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
