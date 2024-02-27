from confluent_kafka import Consumer, KafkaError

def main():
    running = True
    topic = '/telecom/mystream:mytopic'
    consumer = Consumer({'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'earliest'}} )

    consumer.subscribe([topic])

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue
  
        if not msg.error():
            print('Received message: %s' % msg.value().decode('utf-8'))
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    
    consumer.close()


if __name__ == "__main__":
    main()
