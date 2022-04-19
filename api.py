from flask import Flask, abort, request
from flask import jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#Base de datos 
app = Flask(__name__)

tasks = [
    {
        "id": 1,
        "name": "Tomar la clase",
        "check": False,
        "updated": None,

    },
    {
        "id": 2,
        "name": "Hacer la tarea",
        "check": False,
        "updated": None,
    },
]

@app.route('/')
def hello_world():
    return '<h1>----- Bienvenido a mi API To-Do End-User -----</h1>'


@app.route('/api/tasks/', methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})


@app.route('/api/tasks/<int:id>', methods=["GET"])
def get_task(id):
    this_task = [task for task in tasks if task["id"] == id]
    return (
        jsonify({"task": this_task[0]})
        if this_task
        else jsonify({"status": "ID Inexistente"})
    )


@app.route('/api/tasks/', methods=["POST"])
def create_task():
    if not request.json:
        abort(404)
    task = {
        "id": len(tasks) + 1,
        "name": request.json["name"],
        "check": False,
   
    }
    tasks.append(task)
    return jsonify({"tasks": tasks}), 201


@app.route('/api/tasks/<int:task_id>', methods=["PUT"])
def update_task(task_id):
    if not request.json:
        abort(400)

    this_task = [task for task in tasks if task["id"] == task_id]

    if not this_task:
        abort(404)

    if "name" in request.json and type(request.json.get("name")) is not str:
        abort(400)

    if "check" in request.json and type(request.json.get("check")) is not bool:
        abort(400)

    this_task[0]["name"] = request.json.get("name", this_task[0]["name"])
    this_task[0]["check"] = request.json.get("check", this_task[0]["check"])



    return jsonify({"task": this_task[0]}), 201


@app.route('/api/tasks/<int:task_id>', methods=["DELETE"])
def delete_task(task_id):
    this_task = [task for task in tasks if task["id"] == task_id]

    if not this_task:
        abort(404)

    tasks.remove(this_task[0])
    return jsonify({"result": True})

def show_task():
    try:
        response = requests.get(url)
        print(response.status_code)
        return response.json()['tasks']
    except requests.exceptions.HTTPError as err:
        print("Error.")
        raise SystemExit(err)
    except requests.exceptions.ConnectionError as err:
        print(f"----- Error! {err}") 
    except requests.exceptions.JSONDecodeError as err:  
        print(f"----- Error de JSONDecodeError! {err}") 
def create_task(task):
    try:
        response = requests.post(url, json={"name": task})
        print(response.status_code)
        return response.json()['tasks']
    except requests.exceptions.HTTPError as err:
        print("Error...!")
        raise SystemExit(err)
    except requests.exceptions.ConnectionError as err:
        print(f"----- ERROR! {err}")
    except requests.exceptions.JSONDecodeError as err:
        print(f"----- ERROR JSONDecodeError! {err}")


url = 'http://127.0.0.1:5000/api_orm_bd/tasks'
op_salir = True


while op_salir:
    print("--- Menu de mi API End User ---")
    print("1. Mostrar tarea de end user: ")
    print("2. Crear tarea de end user: ")
    print("3. Salir del programa: ")
    print("\n")
    op = int(input("Escoga una opcion: "))
    #except ValueError as e:
     #  op = 0

    if(op == 1):
        data = show_task()
        for task in data:
            print(task)
    elif(op == 2):
        data = create_task(input("Ingrese la tarea:  \n"))
        for task in data:
            print(task) 
    elif(op == 3):
        op_salir = False
        print("Saliendo del programa...")  
    else:
         print("La opcion que ingresaste es invalida")   


    