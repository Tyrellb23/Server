from flask import Flask, redirect, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("https://www.google.com")

# Serve favicon from static folder
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico')

if __name__ == "__main__":
    app.run()
