import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)
DATA_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

@app.route("/")
def home():
    return "Hello, To-Do App!"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    title = request.json.get("title", "").strip()
    if not title:
        return jsonify(error="title is required"), 400
    tasks = load_tasks()
    new_id = max([t["id"] for t in tasks], default=0) + 1
    task = {"id": new_id, "title": title, "done": False}
    tasks.append(task)
    save_tasks(tasks)
    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def toggle_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = not t["done"]
            save_tasks(tasks)
            return jsonify(t)
    return jsonify(error="not found"), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    tasks = [t for t in load_tasks() if t["id"] != task_id]
    save_tasks(tasks)
    return jsonify(message="deleted")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)