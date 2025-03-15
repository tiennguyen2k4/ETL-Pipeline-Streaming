from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType
def spark_connection():
    spark = None
    try:
        spark = SparkSession.builder \
        .appName("spark_kafka") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.2") \
        .getOrCreate()
        print("Connect to kafka successfully")
    except Exception as e:
        print(f"Could not connect to kafka! please check again: {e}")
    return spark

def read_data_from_kafka():
    spark_df = None
    spark = spark_connection()
    try:
        spark_df = spark.readStream \
        .format('kafka') \
        .option('kafka.bootstrap.servers','broker:9092') \
        .option('subscribe','top_1') \
        .option('startingOffsets','earliest') \
        .option("maxOffsetsPerTrigger", 100) \
        .load()
        print("Read data successfully!!!")
    except Exception as e:
        print(f"Could not read data from kafka! Pleas check again: {e}")
    return spark_df

def write_data():
    spark_df = read_data_from_kafka()
    if spark_df is None:
        print("Kafka DataFrame is None. Check Kafka connection or Spark JARs.")
        return
    spark_df = spark_df.selectExpr("CAST(key AS STRING)","CAST(value AS STRING)")

    schema = StructType([
        StructField("first_name", StringType(), True),
        StructField("last_name", StringType(), True),
        StructField("gender", StringType(), True),
        StructField("street", StringType(), True),
        StructField("city", StringType(), True),
        StructField("country", StringType(), True),
        StructField("postcode", StringType(), True),
        StructField("latitude", StringType(), True),
        StructField("longitude", StringType(), True),
        StructField("email", StringType(), True),
        StructField("phone", StringType(), True),
        StructField("username", StringType(), True),
        StructField("password_hash", StringType(), True),
        StructField("date_registered", StringType(), True)
    ])

    parsed_df = spark_df.select(
        col("key"),
        from_json(col("value"), schema).alias("data")
    ).select("key", "data.*")

    try:
        result = parsed_df.writeStream \
            .outputMode('append') \
            .format('json') \
            .option('path', 'hdfs://namenode:9000/userdata/hdfs/data_output/') \
            .option('checkpointLocation', 'hdfs://namenode:9000/user/hdfs/checkpoints/') \
            .start()
        print("Write to console successfully!!!")
        result.awaitTermination()
    except Exception as e:
        print(f"Could not write to console!! Please check again: {e}")

if __name__ == '__main__':
    write_data()



