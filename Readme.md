# Flask Web Application
This is a simple project which uses Flask to create a web application that accepts tasks from Clients. Flask exposes microservice endpoints which acts like a Task master to keep a record of tasks/orders each time a user adds/deletes/updates orders. There is a few functionalities:
1. Adds a new task
2. Update a new task
3. Delete a new task

Each time an order is received, Flask sends them to backend database Flask-SQLAlchemy (Webpage -> Flask -> SQLAlchemy DB). The Flask Web application can either be deployed by the following:
1. Docker containers of nginx and flask web application under ```docker-compose.yml```
2. Kubernetes Cluster service which hosts the following
    - NodePort service
    - Flask Web Application


## Project File Directory
1. ```app.py```
    - Runs Flask Web Application with WSGI server ```waitress```
2. templates folder
    - ```base.html``` - sub-boiler HTML template used for HTML web templates (Run ```html 5``` in VSC for premade template)
    - ```index.html``` - builds upon ```base.html```
    - ```update.html``` - this is for updating the webpage based on update button
3. ```Static\css\main.css```
    - For setting up CSS Styling
4. ```instance/database.db```
    - SQLAlchemy database as an extension of Flask app to store user inputs from internal HTML website
6. ```requirements.txt```
    - Installing all packages needed for this project
7. ```Dockerfile```
    - Build Flask Web application "app.py" IMAGE
8. ```nginx.conf```
    - Configuring nginx as a reverse proxy load balancer and which port to route to our server on
8. ```docker-compose.yml```
    - Build Flask and Nginx CONTAINERS
9. ```kubernetes.yml```
    - Building our kubernetes NodePort service and Deployment (replicas of 2 flask web applications)


## Docker Containers Deployment
The system design is as follows:
1. Create a ```nginx``` service which acts as our reverse proxy load balancer. ```nginx``` first receives client requests and then routes them to our WSGI Server ```waitress```
2. WSGI server ```waitress``` then routes requests to our backend flask application before sending the response back to our WSGI server and finally back to our ```nginx``` again

Please see the following for more details on deployment:
1. Deploy an ```nginx``` container under ```docker-compose.yml``` 
    - We specify the Port forwarding of 8000 in our ```nginx.conf``` file per the line ```proxy_pass http://localhost:8000```
2. Create a docker image for our flask web application by creating a ```Dockerfile``` first
    - ```Dockerfile``` builds our app dependencies by running ```RUN pip install -r requirements.txt```
    - Under our ```app.py```, the code ```serve(app, host='0.0.0.0', port= 8000)``` means we host our flask web application on ```http://localhost:8000``` via our WSGI server ```waitress```
3. Run the docker command ```docker-compose up --build``` which will then build 2 containers: one for ```nginx``` and the other for our ```flask``` web application
4. Push the docker image to DockerHub once you have created the docker containers from above step, which our ```docker-compose```. This is useful if you are using Kubernetes deployment and under the ```Kubernetes.yml``` file, we specify the line ```image: bryanmoh/flask_web-application-web```


## Kubernetes Cluster Deployment
The deployment details are as follows:
1. Create a ```NodePort``` service which sits on Port ```31500``` and forwards it to targetPort = ```8000``` where our flask application pods are at
2. Create a ```Deployment``` where we have 2 replicas of our flask web application pods that seeks to load balance the requests received
3. Run the command ```kubectl create -f kubernetes.yml``` which will create a Kubernetes Cluster which consists of the following below:
    - Run the command ```kubectl get pods```
        - ![alt text](<images/Kubernetes Pods.png>)
    - Run the command ```kubectl get service```
        - ![alt text](<images/Kubernetes Service.png>)
    - Note we have 2 instances of flask web applications because of replica set defined
4. Check if our NodePort is correctly forwarding requests to our Pods
    - Run the command ```kubectl get po -o wide``` first which will get IP address of the Pod
        - ![alt text](<images/Kubernetes Pods endpoint.png>)
    - Run the command ```kubectl get ep python-web-svc``` next to get service endpoint and IP address should match the above
        - ![alt text](<images/Kubernetes Service Endpoint.png>)
        - If done correctly, it should port forward to ```8000``` where our Flask web application in Pod is listening to
5. Port forward to the service by running ```kubectl port-forward service/python-web-svc 8080:80``` which forwards port 8080 to 80. Open up ```http://localhost:8080``` next and you'll see the following:
    - ![alt text](<images/Kubernetes Port Forward.png>)
    - ![alt text](<images/Flask Web App.png>)


## Important notes
1. templates folder
    - ```base.html``` is where we create HTML5 boiler plate 
        - ```{% block head %}{% endblock %}``` and ```{% block head %}{% endblock %}``` is for overriding specific parts of base HTML template for head and body tags 
    - ```index.html``` inherits web template from ```base.html```
2. ```instance/database.db```
    - This is created using Flask SQLALCHEMY with an instance of it initialised via the flask request:
    ```
    @app.before_first_request
    def create_tables():
        db.create_all()
    ```

# References
1. https://github.com/jakerieger/FlaskIntroduction
2. https://github.com/K8sAcademy/Fundamentals-HandsOn/tree/main/L22-02%20Selectors
3. https://github.com/adeola2020-git/python-flask-docker-kubernetes/tree/master
