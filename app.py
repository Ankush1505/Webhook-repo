import certifi
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dateutil import parser
import os
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

MONGO_URI = "mongodb+srv://ankushsarsswat2002_db_user:ankush123@cluster0.wfhnmn0.mongodb.net/?appName=Cluster0" 

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client['techstax_db'] 
collection = db['events']


@app.route('/webhook', methods=['POST'])
def webhook():

    """
    GitHub Webhook Listener Endpoint
    This endpoint receives POST payloads directly from GitHub events.
    ---
    tags:
      - Webhook Operations
    consumes:
      - application/json
    parameters:
      - in: body
        name: payload
        required: true
        description: The JSON payload sent by GitHub
        schema:
          type: object
          properties:
            zen:
              type: string
              example: "Responsive is better than fast."
            repository:
              type: object
              properties:
                name:
                  type: string
                  example: "TechStaX-Webhook"
    responses:
      200:
        description: Webhook payload received and processed successfully.
      400:
        description: Invalid JSON payload.
    """
    
    data = request.json

    if not data:
        return jsonify({"msg": "No data received"}), 400
    
    delivery_id = request.headers.get('X-Github-Delivery')

    if collection.find_one({"delivery_id" : delivery_id}):
        print(f"Duplicate webhooks Blocked : {delivery_id}")
        return jsonify({"Reason" : "Duplicate Ignored"}), 200

   
    event_type = request.headers.get('X-GitHub-Event')

    record = {}

   
    if event_type == 'push':
        author = data['pusher']['name']
        to_branch = data['ref'].split('/')[-1] 
        timestamp = parser.parse(data['head_commit']['timestamp'])
        
        msg = f'"{author}" pushed to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
        record = {
            "type": "PUSH",
            "author": author,
            "to_branch": to_branch,
            "timestamp": timestamp,
            "message": msg
        }

    
    elif event_type == 'pull_request':
        action = data['action']
        pr = data['pull_request']
        author = pr['user']['login']
        from_branch = pr['head']['ref']
        to_branch = pr['base']['ref']
        timestamp = parser.parse(pr['updated_at'])

        
        if action == 'closed' and pr['merged'] == True:
            msg = f'"{author}" merged branch "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
            record = {
                "type": "MERGE",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "message": msg
            }
        
        
        elif action in ['opened', 'edited', 'reopened']:
            msg = f'"{author}" submitted a pull request from "{from_branch}" to "{to_branch}" on {timestamp.strftime("%d %B %Y - %I:%M %p UTC")}'
            record = {
                "type": "PULL_REQUEST",
                "author": author,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
                "message": msg
            }

   
    if record:
        record['delivery_id'] = delivery_id
        collection.insert_one(record)
        print(f" Saved Event: {record['message']}")
    
    return jsonify({"status": "success", "message": "Event logged"}), 200



@app.route('/events', methods=['GET'])
def get_events():
    
    events = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10))
    return jsonify(events)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    
    app.run(debug=True, port=50001)