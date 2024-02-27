import pyspark
from delta import *

appName = "IngestBaseStation"
fileType = "csv"
fileHeader = True
fileSchema = True
fileDelimiter = ","
fileLocation = "/telecom/data/basestation.csv"
targetTable = "/telecom/basestations"
tableCheckpointPath = "/telecom/_checkpoints/csv2base"

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

#  df.write
#   .format("com.mapr.db.spark.streaming") \
#    .option("checkpointLocation", tableCheckpointPath) \
#    .option("tablePath", tablePath) \
#    .option("idFieldPath", "base") \
#    .option("bulkMode", True) \
#    .option("sampleSize", 100) \
#    .option("createTable", False) \
#    .mode("overwrite") \
#    .save(targetTable) 
    
  spark.saveToMapRDB(df, targetTable, id_field_path="id", create_table=False, bulk_insert=True)
  df.show()
  

if __name__ == '__main__':
  main()
