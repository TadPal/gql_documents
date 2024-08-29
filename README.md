# Running Dspace

Pull this repository from github <a>https://github.com/TadPal/UOIS_Dspace_Fork

### Build DSpace
```bash
docker compose -f docker-compose.yml -f docker-compose-cli.yml build
```

### Run DSpace with Angular frontend
```bash
docker compose -p d8 -f docker-compose.yml -f dspace/src/main/docker-compose/docker-compose-angular.yml up -d
```

## Import test data
### Create an admin account.  By default, the dspace-cli container runs the dspace command.
```
docker compose -p d8 -f docker-compose-cli.yml run --rm dspace-cli create-administrator -e test@test.edu -f admin -l user -p admin -c en
```

### Download a Zip file of AIP content and ingest test data
```
docker compose -p d8 -f docker-compose-cli.yml -f dspace/src/main/docker-compose/cli.ingest.yml run --rm dspace-cli
```

### Now you can use dspace as a part of the federation
---

## ISDatabase

Database backend for university site. Project is based on SQLAlchemy and GraphQL (strawberry federated).
<br/><br/>
This project contains only SQLAlchemy models and GraphQL endpoint to provide data from the postgres database running in separate container. To successfully start this application you need to have a running postgres database (for instance in docker container).
<br/><br/>

Start the app inside the docker using docker-compose.yml (recommended)

- to start the app as a docker container you first need to create the gql_core image - to do this use following command:
  docker build -t gql_core .
- this image contains our solution with SQLAlchemy models and GraphQL endpoint
- (optional) you can run the container standalone on any port you want by using: docker run -p your_port:8001 gql_core
- use docker-compose.yml file to set up postgres database and gql_core using this command:
  docker-compose up
- docker will use given compose file to create two containers (isdatabase_gql_entry_point and isdatabase_database)
- gql_entry_point is based on the gql_core image and provides the GraphQL endpoint (contains all our code)
- database container is based on postgres 13.2 image and provides a database (image will be downloaded if necessary)
- postgres is automatically set up by docker-compose.yml - there you can edit variables such as database name, username and password - these will be used by gql to acess the database
- these two containers are able to exchange data between each other on closed docker network
- only gql endpoint is available for other device outside of docker network - to access the GraphQL UI open http://localhost:82/gql on your device
  <br/><br/>

- in this version of our project the database is populated with random data (not all database is populated - for testing purposes only)
  <br/><br/>

pytest --cov-report term-missing --cov=gql_documents tests

Linux demo run:
DEMO=true uvicorn main:app --reload
