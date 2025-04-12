
# API REST para Gestión de Tareas

## Estructura del Proyecto

A continuación, se describe la estructura de los archivos y directorios principales del proyecto:
```
├── app/
│   ├── init.py             # Inicialización de la aplicación Flask
│   ├── models.py           # Definición de los modelos de la base de datos (Task, Priority, State)
│   ├── schemas.py          # Definición de los schemas de validación y serialización (usando Marshmallow)
│   └── routes.py           # Definición de las rutas de la API y la lógica de los endpoints
├── instance/
│   └── config.py           # Archivo de configuración específico de la instancia
├── requirements.txt        # Lista de dependencias de Python necesarias para el proyecto
├── populate_db.py          # Script auxiliar para popular la base de datos
├── run.py                  # 
└── README.md               # Este archivo
```

## Comandos para Correr la API

A continuación, se detallan los pasos para configurar y ejecutar la API REST en tu entorno local:

1.  **Clonar el Repositorio:**

    ```bash
    git clone https://github.com/Pykto/task-app-backend.git
    cd task-app-backend
    ```

2.  **Crear un Entorno Conda:**

    ```bash
    conda create --name task-app python=3.13 
    ```

3.  **Activar el Entorno Conda:**

    ```bash
    conda activate task-app
    ```

4.  **Instalar las Dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **Configurar la Base de Datos (Usando Variables de Entorno):**

    Archivo `.env` en la raíz del proyecto:

    ```
    DATABASE_USER=<tu_usuario_de_base_de_datos>
    DATABASE_PASSWORD=<tu_contraseña_de_base_de_datos>
    DATABASE_HOST=<el_host_de_tu_base_de_datos>
    DATABASE_NAME=<el_nombre_de_tu_base_de_datos>
    FLASK_APP=run.py
    FLASK_DEBUG=True
    ```

5.  **Ejecutar la Aplicación Flask:**
    ```bash
    flask run
    ```

## Endpoints de la API

A continuación, se listan los endpoints principales de la API:

* **`POST /tareas`**: Crea una nueva tarea.
    * **Cuerpo de la Solicitud (JSON):**
        ```json
        {
            "title": "Título de la tarea",
            "description": "Descripción detallada de la tarea",
            "priority": "LOW" | "MEDIUM" | "HIGH" (opcional, por defecto: "MEDIUM"),
            "state": "PENDING" | "IN_PROGRESS" | "COMPLETED" | "CANCELED" (opcional, por defecto: "PENDING"),
            "expiration_date": "YYYY-MM-DDTHH:MM:SSZ" (opcional, en formato ISO 8601 UTC)
        }
        ```
    * **Respuesta (JSON - 201 Created):**
        ```json
        {
            "message": "Successfuly created task",
            "id": <ID_DE_LA_NUEVA_TAREA>
        }
        ```
    * **Respuesta (JSON - 400 Bad Request):** En caso de errores de validación.

* **`GET /tareas`**: Obtiene la lista de todas las tareas.
    * **Respuesta (JSON - 200 OK):**
        ```json
        [
            {
                "id": 1,
                "title": "Tarea 1",
                "description": "Descripción de la tarea 1",
                "priority": "MEDIUM",
                "state": "PENDING",
                "creation_date": "YYYY-MM-DDTHH:MM:SS.ffffff",
                "expiration_date": "YYYY-MM-DDTHH:MM:SSZ" | null
            },
            // ... más tareas
        ]
        ```

* **`GET /tareas/<int:id>`**: Obtiene una tarea específica por su ID.
    * **Parámetro de la URL:** `id` (entero)
    * **Respuesta (JSON - 200 OK):** Los detalles de la tarea.
    * **Respuesta (JSON - 404 Not Found):** Si la tarea con el ID especificado no existe.

* **`PUT /tareas/<int:id>`**: Actualiza una tarea existente por su ID.
    * **Parámetro de la URL:** `id` (entero)
    * **Cuerpo de la Solicitud (JSON):** Los campos a actualizar (opcional).
        ```json
        {
            "title": "Nuevo título",
            "description": "Nueva descripción",
            "priority": "HIGH",
            "state": "IN_PROGRESS",
            "expiration_date": "YYYY-MM-DDTHH:MM:SSZ"
        }
        ```
    * **Respuesta (JSON - 200 OK):**
        ```json
        {
            "message": "Tarea actualizada con éxito",
            "id": <ID_DE_LA_ TAREA_ACTUALIZADA>
        }
        ```
    * **Respuesta (JSON - 404 Not Found):** Si la tarea con el ID especificado no existe.
    * **Respuesta (JSON - 400 Bad Request):** En caso de errores de validación.

* **`DELETE /tareas/<int:id>`**: Elimina una tarea existente por su ID.
    * **Parámetro de la URL:** `id` (entero)
    * **Respuesta (JSON - 200 OK):**
        ```json
        {
            "message": "Successfully deleted task",
            "id": <ID_DE_LA_ TAREA_ELIMINADA>
        }
        ```
    * **Respuesta (JSON - 404 Not Found):** Si la tarea con el ID especificado no existe.

---