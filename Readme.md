# Key Account Manager (KAM) Lead Management System Project

The Key Account Manager (KAM) Lead Management System is a comprehensive software solution designed to streamline the management and nurturing of high-value client accounts. The system empowers Key Account Managers to efficiently track, manage, and optimize their interactions with key clients, ensuring a more personalized and strategic approach to customer relationships.

## Requirements

- Python 3.12 or above

## Setup Instructions

Follow these steps to set up the project:

### 1. Create a Virtual Environment

To begin, create a virtual environment for the project by running:

```bash
python -m venv venv
```

Activate the virtual environment:

- On **Windows**:

  ```bash
  .\venv\Scripts\activate
  ```

- On **macOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 2. Install the Required Dependencies

With the virtual environment activated, install the dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Configure the Database Parameters

You need to configure your database parameters. You can choose one of the following methods to provide these details:

- **Option 1: Using a `.env` file**

  Create a `.env` file in the root directory of your project and add your database configuration as follows:

  Example `.env`:

  ```
  DB_TYPE=postgresql
  DB_HOST=your_db_host
  DB_PORT=your_db_port
  DB_USER=your_db_user
  DB_PASSWORD=your_db_password
  DB_NAME=your_db_name
  ```

- **Option 2: Using a `config/app.json` file**

  Alternatively, you can add your database configuration to the `config/app.json` file:

  Example `config/app.json`:

  ```json
  {
    "db": {
      "host": "your_db_host",
      "port": "your_db_port",
      "user": "your_db_user",
      "password": "your_db_password",
      "database": "your_db_name"
    }
  }
  ```

Make sure to replace the placeholders with your actual database details.

### 4. Run the Application

Once the dependencies are installed and the database parameters are configured, you can run the application.

- **Option 1: Using `uvicorn`**

  To start the server with `uvicorn`, use the following command:

  ```bash
  uvicorn main:app --reload
  ```

  This will start the FastAPI application in development mode with auto-reloading enabled.

- **Option 2: Running with `python main.py`**

  Alternatively, you can run the app directly with the following command:

  ```bash
  python main.py
  ```

  The application will start and be accessible at `http://127.0.0.1:8000`.

### 5. Testing the Application

```bash
pytest
```

### 6. Access the API Documentation

Once the server is running, you can access the automatically generated API documentation:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

These interfaces will allow you to interact with and test your API.

### 7. Video Link

[Watch the video](https://drive.google.com/file/d/121Ugb5bw0UtxJ7aiEbAE9Plcf4_zDu71/view?usp=sharing)
