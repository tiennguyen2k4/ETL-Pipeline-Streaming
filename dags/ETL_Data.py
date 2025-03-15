from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta
import Stream_Data_To_Kafka

default_args = {
    'owner': 'tiendinh',
    'start_date': datetime(2025,3,1),
    'retries': 3,
    'retry_delay': timedelta(minutes=2)
}

with DAG (
    dag_id = 'my_dag',
    default_args = default_args,
    description = 'DAG transform data user',
    schedule_interval = '@daily',
    catchup = False
) as dag:
    stream_data_to_kafka = PythonOperator(
        task_id='load_data_to_database',
        python_callable=Stream_Data_To_Kafka.stream_data
    )
    write_data_to_hdfs = SparkSubmitOperator(
        task_id='write_data' ,
        application='./dags/Stream_Data_To_HDFS.py' ,
        conn_id='connect_spark' ,
        packages="org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.2" ,
        conf={
            "spark.master": "yarn",
            "spark.submit.deployMode": "client",
            "spark.hadoop.yarn.resourcemanager.address": "resourcemanager:8032",
            "spark.hadoop.fs.defaultFS": "hdfs://namenode:9000",
            "spark.driver.memory": "1g",
            "spark.executor.memory": "2g",
            "spark.executor.cores": "2",
            "spark.yarn.am.waitTime": "600s",
            "spark.rpc.message.maxSize": "1024",
            "spark.hadoop.ipc.maximum.data.length": "536870912",
            "spark.driver.maxResultSize": "2g" ,
            "spark.sql.shuffle.partitions": "2",
            "spark.hadoop.yarn.resourcemanager.scheduler.address": "resourcemanager:8030",
            "spark.hadoop.yarn.resourcemanager.resource-tracker.address":"resourcemanager:8031"
        },
        env_vars={
            "HADOOP_CONF_DIR": "/opt/hadoop/etc/hadoop",
            "YARN_CONF_DIR": "/opt/hadoop/etc/hadoop",
        },
        verbose=True
    )
    stream_data_to_kafka >> write_data_to_hdfs

