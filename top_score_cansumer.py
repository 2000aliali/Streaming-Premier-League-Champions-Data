from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, IntegerType, FloatType

#***************************************************************************************************************************** 

try:
    # Create a SparkSession
    spark = SparkSession.builder \
        .appName("KafkaToPostgres") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    # Define the schema for the Kafka messages
    schema = StructType() \
        .add("rank", IntegerType()) \
        .add("player_name", StringType()) \
        .add("team_name", StringType()) \
        .add("total_goals", FloatType()) \
        .add("total_assists", FloatType()) \
        .add("total_games_played", FloatType()) \
        .add("goal_per_90", FloatType()) \
        .add("mins_per_goal", FloatType()) \
        .add("total_shots", FloatType()) \
        .add("goal_conversion", FloatType()) \
        .add("shot_accuracy", FloatType())

    # Create a DataFrame representing the Kafka stream
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "topic_top_score") \
        .load()

    # Parse the value column of Kafka messages as JSON and apply the defined schema
    df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Define PostgreSQL connection properties
    jdbc_url = "jdbc:postgresql://localhost:5432/premier_league"
    table_name = "top_score2"  # Specify your table name here
    connection_properties = {
        "user": "ali",
        "password": "your password",
        "driver": "org.postgresql.Driver"
    }

    # Write each record from the streaming DataFrame to PostgreSQL table with SaveMode.Overwrite
    query = df\
        .writeStream \
        .outputMode("update") \
        .foreachBatch(lambda batch_df, batch_id: batch_df.write.jdbc(jdbc_url, table_name, mode="append", properties=connection_properties)) \
        .start()

    query.awaitTermination()

except Exception as e:
    print("Error occurred:", e)
