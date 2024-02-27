import io
import csv
import json
import time
import avro.schema
from avro.io import DatumWriter
from datetime import datetime
from confluent_kafka import Producer

def getTime(str):
    if ( len(str) == 10 ):
         str = str + " 00:00"
    return int(datetime.strptime(str,'%d/%m/%Y %H:%M').timestamp())

def buildJSON(row,id):
    return {
        "id": id,
        "startime": getTime(row[0]),
        "endtime": getTime(row[1]),
        "base": row[2],
        "userid": row[3]
    }

def main():
    count = 0
    topic = "calls"
    schemaPath = './resources/call.avsc'
    schema = avro.schema.parse(open(schemaPath, 'r').read())
    producer = Producer( {'streams.producer.default.stream': '/telecom/mystream'} )

    with open('./data/calls.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        for row in reader:
            try:
                data = buildJSON(row,str(count))

                writer = DatumWriter(schema)
                bytesWriter = io.BytesIO()
                encoder = avro.io.BinaryEncoder(bytesWriter)
                writer.write( data, encoder)

                producer.produce( topic, key=data['id'], value=bytesWriter.getvalue()  )
                print(count, end='\r')
                count = count + 1
            except Exception as err:
                print(err)

        producer.flush()
        print("All calls sent to topic")
        print(count)

if __name__ == "__main__":
    main()
