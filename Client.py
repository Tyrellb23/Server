from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return redirect("https://www.google.com")

# Ignore favicon.ico requests with a 204 status
@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content

if __name__ == "__main__":
    app.run()
