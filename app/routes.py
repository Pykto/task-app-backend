from app import app, db
from app.models import Task, Priority, State
from flask import request, jsonify
from datetime import datetime, timezone

#TODO add validation
#TODO add queries for tags

@app.post("/tareas")
def post_task():
    data = request.get_json()

    new_task = Task(
        title = data['title'],
        description = data['description'],
        priority = Priority[data.get('priority', 'MEDIUM').upper()],
        state = State[data.get('state', 'PENDING').upper()],
        expiration_date = datetime.fromisoformat(data.get('expiration_date')).astimezone(
            timezone.utc) if data.get('expiration_date') else None
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Tarea creada con éxito', 'id': new_task.id}), 201


@app.get("/tareas")
def get_tasks():
    tasks = Task.query.all()
    task_list = [{
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority.name,
        'state': task.state.name,
        'creation_date': task.creation_date.isoformat(),
        'expiration_date': task.expiration_date.isoformat() if task.expiration_date else None
    } for task in tasks]
    return jsonify(task_list), 200


@app.get("/tareas/<int:id>")
def get_task(id):
    task = Task.query.get_or_404(id)
    task_data = {
        'id': task.id,
        'title': task.title,
        'description': task.description,
        'priority': task.priority.name,
        'state': task.state.name,
        'creation_date': task.creation_date.isoformat(),
        'expiration_date': task.expiration_date.isoformat() if task.expiration_date else None
    }
    return jsonify(task_data), 200


@app.put("/tareas/<int:id>")
def put_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()

    if data.get('title'):
        task.title = data['title']
    if data.get('description'):
        task.description = data['description']
    if data.get('priority'):
        task.priority = Priority[data['priority'].upper()]
    if data.get('state'):
        task.state = State[data['state'].upper()]
    if data.get('expiration_date'):
        task.expiration_date = datetime.fromisoformat(
            data['expiration_date']).astimezone(timezone.utc)

    db.session.commit()
    return jsonify({'message': 'Tarea actualizada con éxito', 'id': id}), 200


@app.delete("/tareas/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada con éxito', 'id': id}), 200
