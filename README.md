# GitHub Webhook Listener (Live Project)

This is a backend microservice I built to track real-time events on GitHub repositories. 

It listens for "Push" and "Pull Request" events and automatically saves the data to a MongoDB database. It is currently deployed live on Render.

### 🔴 Live Demo
You can see the project running here:
**[https://ankush-webhook.onrender.com](https://ankush-webhook.onrender.com)**

---

### 🚀 What it does
* **Real-time Tracking:** When someone pushes code or merges a PR, this system catches it instantly.
* **Smart Filtering:** It looks at the JSON data from GitHub and only saves the important info (Author, Branch, Timestamp, Commit message).
* **Database Storage:** All events are stored in MongoDB Atlas (NoSQL) so they can be queried later.

### 🛠️ Tech Stack
* **Language:** Python 3.10
* **Framework:** Flask (chosen for simplicity and speed)
* **Database:** MongoDB (using PyMongo)
* **Server:** Gunicorn (to handle multiple requests at once)
* **Hosting:** Render Cloud

### ⚙️ How to run it locally
If you want to test this code on your own machine:

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Ankush1505/webhook-assignment.git](https://github.com/Ankush1505/webhook-assignment.git)
   cd webhook-assignment

2. Install Dependencies:
   pip install -r requirements.txt

   
3. Run The Server:
    python app.py


Built by: ANKUSH


