
# PRODUCER

# conf = {
#     "bootstrap.servers": f"{host}:9092",
#     # "queue.buffering.max.messages": 100000,
#     "acks": 1,
#     "queue.buffering.max.ms": 10,
#     "security.protocol": "SASL_PLAINTEXT",
#     "sasl.mechanism": "PLAIN",
#     "enable.ssl.certificate.verification": "false",
#     "sasl.username": "mapr",
#     "sasl.password": "mapr",
#     "client.id": socket.gethostname(),
# }
# producer = Producer(conf)

# def delivery_report(err, msg):
#     logging.debug(f"Processed: {err if err is not None else msg}")
#     app.storage.general["demo"]["counting"] += 1

# for msg in messages:
#     producer.poll(0)
#     producer.produce(topic, key="id", value=json.dumps(msg).encode(), callback=delivery_report)
#     # logging.debug(f"Sent: {msg}")

# producer.flush()


# CONSUMER
    # conf = {
    #     "bootstrap.servers": f"{host}:9092",
    #     "group.id": "ezshow-consumer",
    #     "auto.offset.reset": "earliest",
    #     "security.protocol": "SASL_PLAINTEXT",
    #     "sasl.mechanism": "PLAIN",
    #     "enable.ssl.certificate.verification": "false",
    #     "sasl.username": "mapr",
    #     "sasl.password": "mapr",
    # }
    # consumer = Consumer(conf)

    # running = True
    # logging.info(f"Getting messages from {topic}")
    # try:
    #     consumer.subscribe([topic])

    #     while running:
    #         msg = consumer.poll(timeout=1.0)
    #         if msg is None:
    #             continue

    #         if msg.error():
    #             if msg.error().code() == KafkaError._PARTITION_EOF:
    #                 # End of partition event, nothing to worry about, just log it
    #                 logging.debug(
    #                     "%% %s [%d] reached end at offset %d\n"
    #                     % (msg.topic(), msg.partition(), msg.offset())
    #                 )
    #             elif msg.error():
    #                 # not concerned about errors, just report it
    #                 yield msg.error()
    #         else:
    #             print(msg)
    #             yield msg
    # finally:
    #     # Close down consumer to commit final offsets.
    #     consumer.close()

    # yield "TASK_COMPLETED"
