FROM python:3.7

WORKDIR /app
COPY . /app

RUN pip install -U -r requirements.txt &&\
    pip install -U -r tests/requirements.txt &&\
    pip install -U pylint pytest-cov coverage coveralls codacy-coverage

RUN if [ ! -e "/app/local_config.py" ]; then \
        cp "/app/local_config.py.template" "/app/local_config.py" ; \
    fi

ENTRYPOINT ["/app/entrypoint.sh"]
EXPOSE 5000
CMD [ "invoke", "app.run", "--no-install-dependencies", "--host", "0.0.0.0" ]
