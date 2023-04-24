from kafkaHandler import Producer, Consumer

kafkaIp = "20.2.81.4"
kafkaPortNo = "19092"

def send_using_kafka(topic,message):
    # producer = KafkaProducer(bootstrap_servers=[kafkaIp+":"+kafkaPortNo],api_version=(0, 10, 1))
    # producer.send(topic, json.dumps(message).encode('utf-8'))

    # waiting for kafka-server to start

    producer = Producer(bootstrap_servers=[kafkaIp+":"+kafkaPortNo])
    producer.send_message(topic, message)
    producer.close()


def receive_using_kafka(topic):

    # consumer = KafkaConsumer(topic, bootstrap_servers=[kafkaIp+":"+kafkaPortNo], auto_offset_reset='earliest', group_id="consumer-group-a")
    # for message in consumer:
    #     print(message.value.decode('utf-8'))

    # reply = next(consumer)
    # message = reply.value.decode('utf-8')
    # message = json.loads(message)
    # return message

    # waiting for kafka-server to start

    consumer = Consumer(bootstrap_servers=[kafkaIp+":"+kafkaPortNo], topic=topic, group_id="consumer-deployer")
    message = consumer.consume_message()
    consumer.close()
    return message
