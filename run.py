from app import app
from flask import Flask
import os

#app = Flask(__name__)

#@app.route("/")
#def index():
#	return "Hello world!"
port = int(os.environ.get('PORT', 8000))
if __name__ == "__main__":
	app.run(threaded=True, port=port)
#app.run(threaded=True, debug=True)
#port = int(os.environ.get('PORT', 5000))
#app.run(host='0.0.0.0', port=port)

#comment for testing purpose
