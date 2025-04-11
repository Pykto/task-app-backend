from app import app, db
from sqlalchemy.exc import OperationalError

if __name__ == '__main__':
    with app.app_context():
        try:
            print("Intentando crear las tablas en la base de datos...")
            db.create_all()
            print("¡Tablas creadas (o ya existían)! No se encontraron errores de creación.")
        except OperationalError as e:
            if "already exists" in str(e).lower():
                print("Las tablas ya existen en la base de datos. No se realizaron cambios.")
            else:
                print(f"Ocurrió un error al crear las tablas: {e}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")