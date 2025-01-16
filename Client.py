from flask import Flask, request

app = Flask(__name__)

@app.route('/log_ip', methods=['POST'])
def log_ip():
    try:
        # Extract the IP address from the POST request payload
        data = request.get_json()
        client_ip = data.get("ip")

        if client_ip:
            # Log the IP address to the console
            print(f"Received IP Address: {client_ip}")

            # Optional: Write the IP address to a file
            with open("received_ips.txt", "a") as file:
                file.write(f"{client_ip}\n")

            return {"status": "success", "message": "IP logged successfully"}, 200
        else:
            return {"status": "error", "message": "No IP provided"}, 400
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
