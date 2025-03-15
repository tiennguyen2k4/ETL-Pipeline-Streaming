from confluent_kafka import Producer
from Collect_Data_User import Transform_Data_User
import time
def stream_data():
    conf = {'bootstrap.servers':'broker:9092'}
    producer = Producer(conf)
    topic = 'top_1'
    curr_time  = time.time()
    while True:
        if time.time() > curr_time + 10:
            break
        try:
            res = Transform_Data_User()
            producer.produce(topic, value=res)
            producer.flush()
            print(f"Sent data to topic: {topic} successfully")
        except Exception as e:
            print(f"Error, please check again: {e}")

if __name__ == '__main__':
    stream_data()



