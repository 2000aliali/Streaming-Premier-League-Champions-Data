# Streaming-Premier-League-Champions-Data



<!-- TABLE OF CONTENTS -->
## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#SystemArchitecture)
- [Tool Used :](#ToolUsed )
- [get started](#getstarted)
- [Results](#license)
<!-- END OF TABLE OF CONTENTS -->




<a name="introduction"></a>
## Introduction
This project emphasizes the creation of a real-time dashboard. It commences by scripting Premier League Champions data from BBC Sport, followed by data cleaning. Subsequently, the data is streamed to Apache Kafka and then to Apache Spark for processing. The processed data is streamed to PostgreSQL for storage. Finally, a robust dashboard is constructed using Streamlit
<a name="SystemArchitecture"></a>
## System Architecture
![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/System%20Architecture.png)



<a name="ToolUsed "></a>
## Tool Used




- **Apache Kafka :** Integral for streaming data from a BBC sport websit, enabling the continuous flow of Premier League Champions data sourced from BBC Sport. Kafka ensures the seamless transfer of raw data, setting the stage for subsequent processing steps.
- **Apache Spark :** Essential for both real-time data processing and streaming tasks. Spark's distributed computing capabilities handle the incoming data streams from Kafka, facilitating efficient analysis and transformation of the Premier League Champions data
- **postgresql:** Serves as the database backend for storing the processed data. PostgreSQL's reliability and scalability ensure that the valuable insights derived from the data processing pipeline are securely persisted for future retrieval and analysis..
- **Pandas:** Empowered to perform data cleaning and preprocessing tasks on the Premier League Champions data. Pandas' versatility enables efficient manipulation and transformation of the raw data, ensuring its readiness for further processing stages
- **Stremlit:** Instrumental in the final stage of the project, Streamlit is utilized to construct a user-friendly and interactive real-time dashboard. Leveraging Streamlit's capabilities, the dashboard provides stakeholders with intuitive access to the analyzed data insights, facilitating informed decision-making and exploration of Premier League Champions statistics and trends

<a name="getstarted"></a>


## Get Started
1. **Clone the repository:**
   ```sh
   git clone https://github.com/2000aliali/Streaming-Premier-League-Champions-Data.git
2. **Create a database**
 ```sh
   createdb -U username  Premier League

```
3. **Connect to your database**
 ```sh
   psql -U username -d Premier League
 ```
4. **install this library**
 ```sh
pip install strealit
pip install pyspark
pip install psycopg2
pip install kafka
pip install json
pip install requests
pip install BeautifulSoup
pip install time

 ```
5. **Start Zookeeper service**
 ```sh

sudo systemctl start zookeeper
```
6. **Start Kafka service**
 ```sh

sudo systemctl start kafka
```


8. **Run the 3 producer**
 ```sh
python top_score_producer.py
python top_assists_producer.py
python producer_final_table.py 
  
 ```


now let us to verify that our topic are created :
 by  :
 ```sh
 ./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
  
 ```
![Screenshot](https://github.com/2000aliali/End-End-data-engineering-Project-streaming-from-random-users-API-to-cassandera/blob/master/images/image%205.png)

### with
- **Kafka Broker:** Part of the Kafka streaming system, it manages message storage, access, and transport.
- **Zookeeper:** A service for distributed setup and coordination, essential for Kafka’s distributed functioning.
- **Schema Registry:** Offers a REST interface to store and fetch Avro schemas, aiding Kafka streams in recognizing record schemas.
- **Control Center**: A web tool for overseeing Kafka setups, allowing data checks, topic generation, and Kafka Connect configuration.
- **Cassandra DB:** A NoSQL database suitable for large-scale, high-speed data spread across multiple nodes, ensuring no sole point of breakdown. Used here so as to load the processed data.
- **PostgresDB:** A relational database employed as Apache Airflow’s metadata storage and also as a versatile data repository.
ETL Service: After dockerizing the pipeline scripts, added the service to Compose for us to automatically update, build, and push the Docker image to DockerHub with GitHub Actions’ CI script.
- **Airflow Webserver:** Airflow’s UI for outlining and overseeing data workflows or DAGs.
- **Scheduler:** Within Airflow, it kickstarts tasks and forms data pipelines, ensuring timely execution or activation by other tasks.
- **End-of-Project Container:** This container is responsible for running our final script, `ali.py`, which exists in the `myenv` directory. Additionally, it consumes messages from our topic named `users_created` and loads our data into the `cassandra_db`.
