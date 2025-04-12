import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError
from flask_cors import CORS
from werkzeug.exceptions import NotFound

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}/{os.getenv('DATABASE_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# TODO add domain 
CORS(app)

@app.errorhandler(NotFound)
def not_found(e):
    return jsonify({"error": "Tarea no encontrada"}), 404

with app.app_context():
    try:
        db.engine.connect()
        print("Successful DataBase conection")

        engine = db.engine
        metadata = db.metadata
        tables_exist = True
        tables_to_create = []

        print(engine)

        for model in db.Model.__subclasses__():
            table_name = model.__tablename__
            if not engine.dialect.has_table(engine, table_name):
                tables_exist = False
                tables_to_create.append(table_name)

        if not tables_exist:
            print("Creating DataBase tables...")
            for table in tables_to_create:
                print(f"- {table}")
            db.create_all()
            print("Tables created")
        else:
            print("Already existing tables")

    except OperationalError as e:
        print(f"DataBase error: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error while DataBase initialization: {e}")
        raise

from app import routes, models