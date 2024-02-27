import pyspark
from delta import *

appName = "Stage_1"
callTable = "/telecom/callTable"
basestationTable = "/telecom/baseStationTable"
targetTable = "/mydata/staging_1"
targetCheckPointPath = targetTable + "/_checkpoints/stage_1"


def main():
    builder = pyspark.sql.SparkSession.builder.appName(appName) \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    stations = spark.read.format("delta").load(basestationTable).alias('stations')
    calls = spark.readStream.format("delta").load(callTable).alias('calls')

    tab = stations.join(calls, calls["base"] == stations["id"]) \
        .select("userid","base","startime","endtime","latitude","longitude") \
        .writeStream \
        .format("delta")  \
        .option("mergeSchema", "true") \
        .option("checkpointLocation", targetCheckPointPath) \
        .start(targetTable)
    
    #staging_1 = DeltaTable.forPath(spark, targetTable)
    #staging_1.vacuum(0.1)

    tab.awaitTermination()

if __name__ == '__main__':
    main()
