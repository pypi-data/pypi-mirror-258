import io
import os
import json
import requests
import avro.schema
import avro.io
from confluent_kafka import Consumer, KafkaError

def main():
    running = True
    topic = 'telecom:calls'
    url = 'http://'+ os.environ['MAPR_CLUSTER'] + ':4242/api/put'
    schemaPath = './data/call.avsc'
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
            
            telemetry = {}
            telemetry['metric'] = "Entries"
            telemetry['timestamp'] = data['startime']
            telemetry['value'] = 1

            tags = {}
            tags['Base'] = data['base'] 
            telemetry['tags'] = tags

            print('Received message: %s' % json.dumps(telemetry))
            requests.post(url, json = telemetry)
        elif msg.error().code() != KafkaError._PARTITION_EOF:
            print(msg.error())
            running = False
    
    consumer.close()


if __name__ == "__main__":
    main()
