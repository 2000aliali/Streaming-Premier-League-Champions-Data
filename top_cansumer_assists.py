from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType ,FloatType

def consume_from_kafka():
    # Create a SparkSession
    spark = SparkSession.builder \
        .appName("KafkaConsumer") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    ''''
    # Define the schema for the Kafka messages
    schema = StructType() \
        .add("rank", StringType()) \
        .add("player_name", StringType()) \
        .add("team_name", StringType()) \
        .add("total_assists", StringType()) \
        .add("total_goals", StringType()) \
        .add("total_games_played", StringType()) \
        .add("chance_created", StringType()) \
        .add("chance_per_90", StringType()) \
        .add("total_passes", StringType()) \
        .add("passes_completed", StringType()) \
        .add("passes_incompleted", StringType()) \
        .add("pass_accuracy", StringType())
        '''

    # Define the schema for the Kafka messages
    schema = StructType() \
        .add("rank", IntegerType()) \
        .add("player_name", StringType()) \
        .add("team_name", StringType()) \
        .add("total_assists", FloatType()) \
        .add("total_goals", FloatType()) \
        .add("total_games_played", FloatType()) \
        .add("chance_created", FloatType()) \
        .add("chance_per_90", FloatType()) \
        .add("total_passes", FloatType()) \
        .add("goal_incompleted", FloatType()) \
        .add("pass_accuracy", FloatType())

    # Create a DataFrame representing the Kafka stream
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "topic_assists") \
        .load()



    # Define PostgreSQL connection properties
    jdbc_url = "jdbc:postgresql://localhost:5432/premier_league"
    table_name = "top_assists"  # Specify your table name here
    connection_properties = {
        "user": "ali",
        "password": "123456789",
        "driver": "org.postgresql.Driver"
    }


    # Parse the value column of Kafka messages as JSON and apply the defined schema
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Write each record from the streaming DataFrame to PostgreSQL table with SaveMode.Overwrite
    query = df \
        .writeStream \
        .outputMode("update") \
        .foreachBatch(lambda batch_df, batch_id: batch_df.write.jdbc(jdbc_url, table_name, mode="append", properties=connection_properties)) \
        .start()

    query.awaitTermination()


consume_from_kafka()
