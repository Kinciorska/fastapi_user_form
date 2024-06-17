# FastAPI User Form App

This application is created to save user information in FlastAPI using both synchronous and asynchronous requests using celery + rabbitmq. 


## Getting Started

Follow these steps to build and run the app.


### Clone the repository
```
git clone https://github.com/Kinciorska/fastapi_user_form.git
```

### Change into the correct directory
```
cd fastapi_user_form
```

### Build the Docker Image:

   Needed environment files:

- .postgres
- .rabbitmq

Environment files should be located in .envs directory, examples of these environment files are available in the same directory.
 
### Build and run the Docker container using
```
docker compose up
```

### Start Celery worker (N - worker number, C - CPU core number)
``` 
docker compose run fastapi celery -A worker.celery_app worker --loglevel=INFO --concurrency=C --autoscale=10,1  -n workerN@%h
``` 
### Technologies
- FastAPI
- PostgreSQL
- RabbitMQ
- Celery
- Docker

#### License
This app is open-source and distributed under the MIT License.
