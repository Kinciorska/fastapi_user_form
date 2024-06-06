# FastAPI User Form App

This application is created to save user information in FastAPI using both synchronous and asynchronous requests with celery + redis. 


## Getting Started

Follow these steps to build and run the app.

Needed environment files:

- .postgres

Environment files should be located in .envs directory, examples of these environment files are available in the same directory.
 

1. Clone the repository
    ```
   git clone https://github.com/Kinciorska/fastapi_user_form.git
    ```
2. Install the necessary dependencies:
    ``` 
   pip install -r requirements.txt
    ```
3. Run Redis Stack in Docker
    ``` 
   docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:7.2.0-v10
    ```
4. Run the app
    ``` 
   fastapi dev
    ```
5. Start celery workers (N times, N - worker number)
   ``` 
   celery -A config.celery_app worker --loglevel=INFO --concurrency=10 -n workerN@%h
    ```

   
### Technologies
- FastAPI
- PostgreSQL
- Celery
- Redis
- SQLAlchemy



#### License
This app is open-source and distributed under the MIT License.
