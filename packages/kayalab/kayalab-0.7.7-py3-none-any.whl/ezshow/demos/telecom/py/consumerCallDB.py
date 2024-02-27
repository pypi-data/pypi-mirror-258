import pyspark
from delta import *
from pyspark.sql.avro.functions import from_avro, to_avro

tablePath = "/telecom/calls"
tableCheckpointPath = "/telecom/_checkpoints/kafka2DB"
streamTopic = "/telecom/mystream:calls"
schemaPath = "./resources/call.avsc"

builder = pyspark.sql.SparkSession.builder.appName("IngestRawTelemetry") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

spark = configure_spark_with_delta_pip(builder).getOrCreate()

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092" ) \
    .option("subscribe", streamTopic) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

jsonFormatSchema = open( schemaPath, "r").read() 

rawData = df.select(from_avro("value",jsonFormatSchema).alias("call")) \
    .select("call.*") \
    .writeStream \
    .format("com.mapr.db.spark.streaming") \
    .option("checkpointLocation", tableCheckpointPath) \
    .option("tablePath", tablePath) \
    .option("idFieldPath", "id") \
    .option("bulkMode", True) \
    .option("sampleSize", 100) \
    .option("createTable", False) \
    .start()

rawData.awaitTermination()
