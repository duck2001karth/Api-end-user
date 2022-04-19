from asyncio import all_tasks
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# Database configurations

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
#sqlite
#mysql://root@localhost/karth

db = SQLAlchemy(app)
mars = Marshmallow(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True)
    check = db.Column(db.Boolean)
 

    def _init_(self, name, check):
        self.name = name
        self.check = check

    def _repr_(self):
        return '<Task %s>' % self.name  
#Create Database

class TaskSchema(mars.Schema):
    class Meta:
        fileds = ('id','name','check')


#Representacion de una sola tarea
task_schema = TaskSchema() 
#Representacion de todas las tareas 
tasks_schema = TaskSchema(many = True)      

#Imprime la los datos de la tabla
all_tasks = Task.query.all() 
print(all_tasks)
db.create_all()

new_task = Task(name='Inserta datos en la base de datos', check=False)
db.session.add(new_task)
db.session.commit()

del_task = Task.query.get_or_404(2)
print(del_task)

update_task = Task.query.get_or_404(3)
update_task.name = "Se debe cambiar"
db.session.commit()

if __name__ == '_main_':
    app.run(debug = True)