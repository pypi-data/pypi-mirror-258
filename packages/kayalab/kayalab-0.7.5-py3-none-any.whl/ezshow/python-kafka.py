from kafka import KafkaProducer
from kafka import KafkaConsumer


def kafka_publish(host: str, topic: str, messages: list):
    producer = KafkaProducer(
        bootstrap_servers=[f"{host}:9092"],
        security_protocol="SASL_PLAINTEXT",
        sasl_mechanism="PLAIN",
        sasl_plain_username="mapr",
        sasl_plain_password="mapr",
        
    )

    logging.info(f"Sending {len(messages)} messages to {topic}")

    for msg in messages:
        try:
            future = producer.send(topic, json.dumps(msg).encode())
            result = future.get(timeout=60)
            print("DEBUG FUTURE", result)
            metrics = producer.metrics()
            print("DEBUG METRICS", metrics)

        except Exception as error:
            logging.warning(error)

        finally:
            app.storage.general["demo"]["counting"] += 1

    producer.flush()


def kafka_consume(host: str, topic: str):

    consumer = KafkaConsumer(bootstrap_servers=[f"{host}:9092"],
                            auto_offset_reset='earliest',
                            security_protocol='SASL_PLAINTEXT',
                            sasl_mechanism='PLAIN',
                            sasl_plain_username='mapr',
                            sasl_plain_password='mapr')

    consumer.subscribe([topic])
    numMsgConsumed = 0
    for _ in range(10):
        records = consumer.poll(timeout_ms=500)
        for topic_data, consumer_records in records.items():
            print(f"ERDINC: {topic_data}: {consumer_records}")
            for consumer_record in consumer_records:
                print("Received message: " + str(consumer_record.value.decode('utf-8')))
                numMsgConsumed += 1
    print("Messages consumed: " + str(numMsgConsumed))
