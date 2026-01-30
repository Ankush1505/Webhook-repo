from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from dateutil import parser
import os

app = Flask(__name__)


MONGO_URI = "mongodb+srv://ankushsarsswat2002_db_user:ankush123@cluster0.wfhnmn0.mongodb.net/?appName=Cluster0" 

client = MongoClient(MONGO_URI)
db = client['techstax_db'] 
collection = db['events']   

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if not data:
        return jsonify({"msg": "No data received"}), 400

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
        collection.insert_one(record)
        print(f" Saved Event: {record['message']}")
    
    return jsonify({"status": "success"}), 200



@app.route('/events', methods=['GET'])
def get_events():
    
    events = list(collection.find({}, {'_id': 0}).sort("timestamp", -1).limit(10))
    return jsonify(events)



@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=50001)