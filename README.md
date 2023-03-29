# JKLnyt_backend

Backend for https://github.com/jantsavlog/JKLnyt_GIT

## Prerequisites:

#### Technologies
- MongoDB <br/>
- Python <br/>

#### Python libraries
- Pymongo <br/>
- Flask <br/>
- BeautifulSoup4 <br/>
- Requests

## Functionality

- Creates a MongoDB database and a collection, then populates it with scraped event data <br/>
- Endpoint displays data from the collection as JSON

## Running locally

#### Windows:

> Install MongoDB, Python and required libs
> 
> set FLASK_APP=app.py <br/>
> set FLASK_ENV=development <br/>
> py -m flask run

#### Check out in browser:

> http://127.0.0.1:5000/get

## Running on a server with seperate Podman/Docker containers

#### 1. Create a network:
> podman network create JKLnyt-network

#### 2. Start Python REST API container and add to the network:
> root(in our repo: src/): podman build --tag jklnyt-docker . <br/>
> root(in our repo: src/): podman run --name JKLnyt --network JKLnyt-network --detach --publish 50001:80 jklnyt-docker:latest  <br/> <br/>

NOTE for --publish: the left-hand port number is the Docker host port(your computer) and the right-hand side is the Docker container port.

#### 3. Start MongoDB container and add to the network:
> podman run --name mongo --network JKLnyt-network --detach mongo

#### 4. Persist containers when user exits:
> loginctl enable-linger 