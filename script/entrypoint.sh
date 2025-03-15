#!/bin/bash
set -e #stop when have issue.

#check exist file requirement
if [ -e "/opt/airflow/requirements.txt" ]; then
  python -m pip install --upgrade pip
  pip install -r /opt/airflow/requirements.txt
fi

#create airflow database
if [ ! -f "/opt/airflow/airflow.db" ]; then
  airflow db init && \
  airflow users create \
    --username admin \
    --firstname admin \
    --lastname admin \
    --role Admin \
    --email admin@example.com \
    --password admin
fi

#upgrade airflow database
airflow db upgrade

#start webserver
exec airflow webserver
