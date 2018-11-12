
RESTful Payments API Example
============================

This is a payments API Example based on the [Flask RESTplus Sample](https://github.com/frol/flask-restplus-server-example)

Docker is required in order to build and play with this demo project, although you might use a python 3.7 virtualenv.

In order to build and test the project please do as follows:

1) Type `make docker` in order to build the project docker image.

2) Type `make docker-test` in order to run the tests suite within the previously built docker image.

3) Type `make run` in order to run the API server listening to port 5000. Please be sure to have this port open, or you might modify the Makefile to set a different port. You can browse the running server at: [http://localhost:5000/api/v1/](http://localhost:5000/api/v1/)

4) Anything else you may review the Makefile or run `make help` for some other tips.


This example is mainly based on modifying the already existing Flask RESTplus Sample aforementioned above. Thus, adding only the required new entities and models, and removing the sample ones.

