import pyspark
from delta import *

appName = "IngestBaseStation"
fileType = "csv"
fileHeader = True
fileSchema = True
fileDelimiter = ","
fileLocation = "/telecom/data/basestation.csv"
targetTable = "/telecom/basestationtable"
targetTableCheckPoint = targetTable + "/_checkpoints/kafka2Raw"

def main():

  builder = pyspark.sql.SparkSession.builder.appName(appName) \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

  spark = configure_spark_with_delta_pip(builder).getOrCreate()

  df = spark.read.format(fileType) \
    .option("inferSchema", fileSchema) \
    .option("header", fileHeader) \
    .option("sep", fileDelimiter) \
    .load(fileLocation)

  df.write.format("delta").mode("overwrite").save(targetTable)
    
  df.show()
  

if __name__ == '__main__':
  main()
