from app import app, db
from app.models import Task, Priority, State
from app.schemas import TaskSchema, TaskUpdateSchema
from flask import request, jsonify
from datetime import datetime, timezone
from marshmallow import ValidationError

task_schema = TaskSchema()
task_update_schema = TaskUpdateSchema()


@app.post("/tareas")
def post_task():
    data = request.get_json()
    try:
        validated_data = task_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_task = Task(
        title=validated_data['title'],
        description=validated_data['description'],
        priority=Priority[validated_data['priority']],
        state=State[validated_data['state']],
        expiration_date=validated_data.get('expiration_date')
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Successfuly created task', 'id': new_task.id}), 201


@app.put("/tareas/<int:id>")
def put_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    try:
        validated_data = task_update_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    if 'title' in validated_data:
        task.title = validated_data['title']
    if 'description' in validated_data:
        task.description = validated_data['description']
    if 'priority' in validated_data:
        task.priority = Priority[validated_data['priority']]
    if 'state' in validated_data:
        task.state = State[validated_data['state']]
    if 'expiration_date' in validated_data:
        task.expiration_date = validated_data['expiration_date']

    db.session.commit()
    return jsonify({'message': 'Successfuly updated task', 'id': id}), 200


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


@app.delete("/tareas/<int:id>")
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Successfully deleted task', 'id': id}), 200
