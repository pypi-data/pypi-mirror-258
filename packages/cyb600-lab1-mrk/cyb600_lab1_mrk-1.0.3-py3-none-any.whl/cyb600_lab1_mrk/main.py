from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return f"The current time is: {current_time}"

def thetime():
    app.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    thetime()