FROM bitnami/spark:latest

USER root

RUN apt-get update && apt-get install -y wget
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.2.1/hadoop-3.2.1.tar.gz && \
    tar -xzf hadoop-3.2.1.tar.gz -C /opt/ && \
    ln -s /opt/hadoop-3.2.1 /opt/hadoop && \
    rm hadoop-3.2.1.tar.gz

ENV PATH="/opt/hadoop/bin:/opt/hadoop/sbin:${PATH}"

ENV HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop
ENV YARN_CONF_DIR=/opt/hadoop/etc/hadoop

USER 1001