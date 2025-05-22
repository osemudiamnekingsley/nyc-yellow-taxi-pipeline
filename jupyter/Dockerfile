FROM jupyter/base-notebook

USER root

RUN apt-get update && apt-get install -y libpq-dev && \
    pip install pandas psycopg2-binary sqlalchemy matplotlib seaborn

USER jovyan
