import io
import avro.schema
import avro.io
from confluent_kafka import Consumer, KafkaError

def main():
    running = True
    topic = '/telecom/mystream:mytopic'
    schemaPath = '/mapr/maprdemo.mapr.io/mydata/resources/call.avsc'
    consumer = Consumer({'group.id': 'mygroup', 'default.topic.config': {'auto.offset.reset': 'earliest'}} )

    consumer.subscribe([topic])
    schema = avro.schema.parse(open(schemaPath, 'r').read())

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue
  
        if not msg.error():  
            bytes_reader = io.BytesIO(msg.value())
            decoder = avro.io.BinaryDecoder(bytes_reader)
            reader = avro.io.DatumReader(schema)
            data = reader.read(decoder)
            print('Received message: %s' % data)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    
    consumer.close()


if __name__ == "__main__":
    main()
