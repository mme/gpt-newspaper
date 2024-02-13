from flask import Flask, jsonify, request
from backend.langgraph_agent import MasterAgent
import os
import os.path

backend_app = Flask(__name__)

@backend_app.route('/', methods=['GET'])
def index():
    return jsonify({"status": "Running"}), 200

@backend_app.route('/generate_newspaper', methods=['POST'])
def generate_newspaper():
    data = request.json
    master_agent = MasterAgent()
    newspaper = master_agent.run(data["topics"], data["layout"])
    return jsonify({"path": newspaper}), 200

@backend_app.route('/generate_newspaper_html', methods=['POST'])
def generate_newspaper_html():
    data = request.json
    master_agent = MasterAgent()
    newspaper = master_agent.run(data["topics"], data["layout"])
    directory = os.path.dirname(newspaper)
    # in directory, find the first html file that is not called newspaper.html
    html = None
    for file in os.listdir(directory):
        if file.endswith(".html") and file != "newspaper.html":
            html = os.path.join(directory, file)
            break

    if html is None:
        # internal server error
        return jsonify({"error": "No newspaper found"}), 500
    
    # return the html
    with open(html) as f:
        return f.read(), 200

# curl request:
# curl -X POST -H "Content-Type: application/json" -d '{"topics": ["Aliens"], "layout": "layout_1.html"}' http://localhost:8000/generate_newspaper_html