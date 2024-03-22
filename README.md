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
![Screenshot](https://github.com/2000aliali/End-End-data-engineering-Project-streaming-from-random-users-API-to-cassandera/blob/master/images/Image1.png)



<a name="ToolUsed "></a>
## Tool Used


- **Data Source:** We use randomuser.me API to generate random user data for our pipeline.
- **Apache Airflow:** sits at the heart of this project, allowing for scheduled or event-driven ETL tasks, thereby streamlining and automating the entire data workflow.
- **Apache Kafka and Zookeeper:** Used for streaming data from a random API and preparing it for transformation.
- **Control Center and Schema Registry:** Helps in monitoring and schema management of our Kafka streams.
- **Cassandra:** Where the processed data will be stored.
- **Pandas:** for Cleaning,preprocessing ,Manipulating and transforming data

<a name="getstarted"></a>


## Get Started
This project focuses on extracting data from random users api "https://randomuser.me/api/"
Follow these steps to get started with the project:
1. **activte the virtual envairement**
    ```sh
     .\myenv\Scripts\Activate   
2. **Clone the repository:**
   ```sh
   git clone https://github.com/2000aliali/End-End-data-engineering-Project-streaming-from-random-users-API-to-cassandera.git
3. **Go to the project folder**
 ```sh
   cd myenv
```
4. **create image**
 ```sh
   docker build -t pandas-image -f Dockerfile.pandas . 
 ```
5. **Build the environment with Docker Compose:**
```sh
   docker-compose up
 ```
And you will get this :
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
