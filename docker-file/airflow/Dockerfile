FROM apache/airflow:2.10.0-python3.11

USER root

RUN apt-get update && apt-get install -y procps
RUN apt-get update && apt-get install -y openjdk-17-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

USER airflow