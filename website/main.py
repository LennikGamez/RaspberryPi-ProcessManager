import json
import os
from flask import Flask,render_template, request, redirect, url_for
from process import Process

processes = []

def read_processes():
    processes.clear()
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, 'static', 'processes.json')
    with open(json_url, "r") as f:
        for process in json.load(f).get("processes"):
            processes.append(Process(process.get("name"), process.get("cmd")))


app = Flask(__name__)

@app.route("/change-status", methods=["POST"])
def change():
    name = request.args.get("name")
    for process in processes:
        if process.name == name:
            if "stop" in request.form:
                process.stop()
                break
            if "start" in request.form:
                process.run()
                break
    return redirect(url_for("manager"))
@app.route("/")
def manager():
    if len(processes) == 0:
        read_processes()
    else:
        for process in processes:
            running = process.running()
            process.is_running = running
    return render_template("index.html", processes=processes)

@app.route("/add-process", methods=["POST"])
def add():
    name = request.form.get("name")
    command = request.form.get("command")
    processes.append(Process(name, command))
    return redirect(url_for("manager"))

@app.route("/load")
def load():
    read_processes()
    return redirect(url_for("manager"))

app.run(debug=True)