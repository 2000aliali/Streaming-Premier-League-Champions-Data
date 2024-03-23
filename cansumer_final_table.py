from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType , FloatType


#***********************************************drop the table *************************
import psycopg2

# Correct the connection parameters


#********************************************************************************************
# Create a SparkSession
spark = SparkSession.builder \
    .appName("KafkaConsumer") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")


# Define the schema for the Kafka messages
schema = StructType() \
    .add("Rank", IntegerType()) \
    .add("Team Name", StringType()) \
    .add("Games Played", IntegerType()) \
    .add("Games Won", IntegerType()) \
    .add("Games Drawn", IntegerType()) \
    .add("Games Lost", IntegerType()) \
    .add("Goals Scored", IntegerType()) \
    .add("Goals Conceded", IntegerType()) \
    .add("Points", IntegerType())

# Create a DataFrame representing the Kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "topic_premier_league") \
    .load()

# Parse the value column of Kafka messages as JSON and apply the defined schema
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")
''''
# Define PostgreSQL connection properties
jdbc_url = "jdbc:postgresql://localhost:5432/premier_league"
table_name = "top_score2"  # Specify your table name here
connection_properties = {
    "user": "ali",
    "password": "123456789",
    "driver": "org.postgresql.Driver"
}
'''
# Define PostgreSQL connection properties
jdbc_url = "jdbc:postgresql://localhost:5432/premier_league"
table_name = "final_table"  # Specify your table name here
connection_properties = {
    "user": "ali",
    "password": "123456789",
    "driver": "org.postgresql.Driver"
}

# Write each record from the streaming DataFrame to PostgreSQL table with SaveMode.Overwrite
query = df \
    .writeStream \
    .outputMode("update") \
    .foreachBatch(lambda batch_df, batch_id: batch_df.write.jdbc(jdbc_url, table_name, mode="append",
                                                                 properties=connection_properties)) \
    .start()


query.awaitTermination()
