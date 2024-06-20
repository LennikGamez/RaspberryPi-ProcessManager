import json
import os
from flask import Flask,render_template, request, redirect, url_for
from process import Process

processes = []

def getJSONURL():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    return os.path.join(SITE_ROOT, 'static', 'processes.json')

def read_processes():
    processes.clear()
    with open(getJSONURL(), "r") as f:
        for process in json.load(f).get("processes"):
            processes.append(Process(process.get("name"), process.get("cmd"), process.get("onStartUp"), process.get("endpoint")))


def addProcessToJson(name, cmd, onStartUp):
    cmd = cmd.split()
    json_file = getJSONURL()
    with open(json_file, 'r') as f:
        data = json.load(f)
        data["processes"].append({"name": name, "cmd": cmd, "onStartUp": onStartUp})
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def changeStartUpInJSON(name, value):
    json_file = getJSONURL()
    # load old data from json
    with open(json_file, 'r') as f:
        data = json.load(f)
        for process in data["processes"]:
            if process["name"] == name:
                process["onStartUp"] = value

    # write new data to json
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)

def removeProcessFromJSON(name):
    json_file = getJSONURL()
    # load old data from json
    with open(json_file, 'r') as f:
        data = json.load(f)
        for process in data["processes"]:
            if process["name"] == name:
                data["processes"].remove(process)
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=4)


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

@app.route("/add-process", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template("addProcess.html")
    else:
        name = request.form.get("name")
        command = request.form.get("command")
        onStartUp = request.form.get("onStartUp")
        processes.append(Process(name, command, onStartUp))
        addProcessToJson(name, command, onStartUp)
        return redirect(url_for("manager"))

@app.route("/load")
def load():
    read_processes()
    return redirect(url_for("manager"))

@app.route("/change-startUp", methods=["POST"])
def change_startUp():
    name = request.args.get("name")
    for process in processes:
        if process.name == name:
            process.start_on_startup = not process.start_on_startup
            changeStartUpInJSON(name, process.start_on_startup)
    return redirect(url_for("manager"))


@app.route("/delete-process", methods = ["POST"])
def delete():
    name = request.args.get("name")
    for process in processes:
        if process.name == name:
            processes.remove(process)
            removeProcessFromJSON(name)
            break
    return redirect(url_for("manager"))

app.run(debug=True)