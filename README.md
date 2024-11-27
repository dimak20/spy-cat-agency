# Spy Cat Agency 🐱

This is a Django REST Framework (DRF) powered API for managing spy missions, targets, and spy cats. The API is designed to handle key functionalities in a secret agent operations system, including mission assignments, target tracking, cat management, and related entities.

The system enables users to:

Create, update, and manage missions.
Assign and update targets for missions.
Manage spy cats, including assigning them to missions.
Track mission completion status and target progress.
This API is designed to ensure efficient tracking of espionage tasks and the management of agents in the field, with robust validation for mission and target states.

## Run service on your machine

1. Clone repository  
```shell
git clone https://github.com/dimak20/spy-cat-agency.git
cd spy-cat-agency
```
2. Then, create and activate .venv environment  
```shell
python -m venv env
```
For Unix system
```shell
source venv/bin/activate
```

For Windows system

```shell
venv\Scripts\activate
```

3. Install requirements.txt by the command below  


```shell
pip install -r requirements.txt
```

4. You need to migrate
```shell
python manage.py migrate
```
5. (Optional) Also you can load fixture data
```shell
python manage.py loaddata data.json
```


6. And finally, run server

```shell
python manage.py runserver # http://127.0.0.1:8000/
```

## Run with Docker

1. Clone repository  
```shell
git clone https://github.com/dimak20/spy-cat-agency.git
cd spy-cat-agency
```
2. Create .env file and set up environment variables
```shell
DATABASE_ENGINE=postgresql
POSTGRES_PASSWORD=password
POSTGRES_USER=user
POSTGRES_DB=db
POSTGRES_HOST=db
POSTGRES_PORT=5432
PGDATA=/var/lib/postgresql/data/pgdata
DJANGO_SECRET_KEY=your_secret_key
USE_REDIS=false
```

3. Build and run docker containers 


```shell
docker-compose -f docker-compose.yaml up --build
```

4. (Optionally) You can load data inside docker container and 

```shell
docker exec -it <your_container_name> sh
python manage.py loaddata data.json
```

You can find out container name by the command "docker ps" -> your cat service id

5. Access the API at http://localhost:8000/api/v1/

## API Endpoints
You can download the endpoints schema by the link below or download it directly from the repository:

- [Postman Collection on Dropbox](https://www.dropbox.com/scl/fi/cbyf3zq4dz876vjvbamia/Spy-Cat-Agency-API.yaml?rlkey=kcqcnlizuv4fuw7b307wtx38s&st=phdbk1v0&dl=0)





### Project configuration

Your project needs to have this structure


```plaintext
Project
├── spycats
|   └── management
|   |  └── commands
|   |     └── wait_for_db.py
|   |── tests
│   ├── __init__.py
│   └── admin.py
│   ├── apps.py
|   ├── filters.py
|   ├── models.py
│   ├── validators.py
|   ├── serializers.py
|   ├── utils.py
│   ├── urls.py
│   └── views.py
|
|
├── spy_cat_agency
│   ├── __init__.py
│   ├── asgi.py
│   ├── asgi.py
│   ├──celery.py
│   ├── settings.py
│   └── urls.py
│   
├── media
│   
├── logos
│   
├── templates
|
│
├── .dockerignore
│
├── .env
│
├── .gitignore
│
│
├── docker-compose.yaml
│
├── Docker
│
├── manage.py
│
│
├── README.md
|
└── requirements.txt
```