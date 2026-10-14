from flask import Flask

# Create a simple app for testing
app = Flask(__name__)

@app.route('/')
def hello():
    return "Doom Web Crawler System is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)