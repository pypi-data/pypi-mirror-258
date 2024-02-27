import io
import csv
import json
import time
import avro.schema
from avro.io import DatumWriter
from datetime import datetime
#from kafka import KafkaProducer
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

count = 0
schema = avro.schema.parse(open("./resources/call.avsc", 'r').read())
#producer = KafkaProducer( bootstrap_servers = ['maprdemo.mapr.io:9092'] )
producer = Producer( {'streams.producer.default.stream': '/telecom/mystream'} )

with open("./data/calls.csv", 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    header = next(reader)
    for row in reader:
        data = buildJSON(row,str(count))
        writer = DatumWriter(schema)
        bytesWriter = io.BytesIO()
        encoder = avro.io.BinaryEncoder(bytesWriter)
        writer.write( data, encoder)          
        producer.produce( "calls", key=data['id'], value = bytesWriter.getvalue()  )
        producer.flush()
        count = count + 1
