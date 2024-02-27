import pyspark
from delta import *
from pyspark.sql.avro.functions import from_avro, to_avro

appName = "IngestRawTelemetry"
streamTopic = "/telecom/mystream:calls"
schemaPath = "./resources/call.avsc"
targetTable = "/telecom/callTable"
targetTableCheckPoint = targetTable + "/_checkpoints/kafka2Raw"



def main():
    builder = pyspark.sql.SparkSession.builder.appName(appName) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
	.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    df = spark.readStream.format("kafka") \
	.option("kafka.bootstrap.servers", "localhost:9092" ) \
	.option("subscribe", streamTopic) \
	.option("startingOffsets", "earliest") \
	.option("failOnDataLoss", "false") \
        .option("maxFilesPerTrigger", 1) \
	.load()

    jsonFormatSchema = open(schemaPath,"r").read()

    rawData = df.select(from_avro("value",jsonFormatSchema).alias("call")) \
        .select("call.*") \
        .writeStream \
        .format("delta") \
        .outputMode("append") \
        .option("mergeSchema", "true") \
        .option("checkpointLocation",targetTableCheckPoint)  \
        .trigger(processingTime='2 seconds') \
        .start(targetTable)
  
    rawData.awaitTermination()


if __name__ == '__main__':
    main()
