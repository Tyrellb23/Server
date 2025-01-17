import requests
import json

# Server URL to send the IP address
SERVER_URL = "http://your-server-url/log_ip"

def get_public_ip():
    """
    Get the public IP address of the client using an external API.
    """
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        public_ip = response.json().get("ip")
        return public_ip
    except requests.RequestException as e:
        print(f"Error fetching public IP: {e}")
        return None

def send_ip_to_server(ip):
    """
    Send the public IP address to the server via POST request.
    """
    try:
        payload = {"ip": ip}
        headers = {"Content-Type": "application/json"}
        response = requests.post(SERVER_URL, data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print(f"Server response: {response.json()}")
    except requests.RequestException as e:
        print(f"Error sending IP to server: {e}")

def main():
    """
    Main function to get and send the public IP address.
    """
    public_ip = get_public_ip()
    if public_ip:
        print(f"Your public IP is: {public_ip}")
        send_ip_to_server(public_ip)
    else:
        print("Unable to determine public IP.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)
