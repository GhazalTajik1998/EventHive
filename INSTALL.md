# Installation guide

This guide provides instructions for installing and setting up the Project Name API on your local machine.

## Prerequisites
- Python 3.7 or higher
- pip
- RabbitMQ

## Installation
1. Clone the repository:
``` bash:
git clone https://github.com/ghazaltajik1998/EventHive.git
```
2. Change to the project directory:
``` bash:
cd EventHive
```
3. Create a virtual enviroment:
``` bash:
python -m venv venv
```
4. Activate the virtual enviroment:
- On macOS/Linux:
    ``` bash:
    source venv/bin/activate
    ```
- On Windows:
``` bash:
venv\Scripts\activate.bat
```
5. Install the dependencies:
``` bash:
pip install -r requirements.txt
```
6. Run the database migrations:
``` bash:
python manage.py migrate
```
7. Start the RabbitMQ service:
``` sql:
sudo systemctl start rabbitmq-server
```
8. Start the Celery worker :
``` bash:
celery -A backend worker --loglevel=INFO -P eventlet
```
9. Start the development server:
``` bash:
python manage.py runserver
```


## Usage
Once the API is set up and running, you can access it at http://localhost:8000. You can use the Swagger documentation at http://localhost:8000/swagger/ to explore the API's endpoints and functionality.

## Testing
To run the tests included in the project, run :
``` bash:
python manage.py test
```

