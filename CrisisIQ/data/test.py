import json

tasks = json.load(open("tasks.json"))
print(tasks[0])