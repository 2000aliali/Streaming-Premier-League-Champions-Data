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
![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/Capture%20d'%C3%A9cran%202024-03-24%20005641.png)

 9. **Run**
 ```sh
 spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --jars postgresql-driver.jar  top_score_cansumer.py
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --jars postgresql-driver.jar  top_score_producer.py
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 --jars postgresql-driver.jar  cansumer_final_table.py 
 ```
 10. **Run**
 ```sh
streamlit run premier_league_dashbooard.py
 ```

<a name="license"></a>
## Results
verify that the tables are created in postgresql


![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/Capture%20d'%C3%A9cran%202024-03-24%20012006.png)
 then go to http://localhost:8501 to dispaly a real time dashbording
first there is a general dashboard for the prmeir league and also a dasboard for any team in the premier league :
  ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/first.png)
  if you select genral dashbooared : 
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/img1.png)
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/img2.png)
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/img3.png)
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/img4.png)
   And if you selected dasbooard team :
     first hcosse your best team 
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg1.png)
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg2.png)
    ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg3.png)
     ![Screenshot](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg4.png)



 


 # Verification of Tables in PostgreSQL

1. **Ensure Tables Creation**: Verify that the tables are created in PostgreSQL by querying the database using SQL commands or using a database management tool like pgAdmin.

# Real-Time Dashboard Access

2. **Access the Dashboard**: After verifying the tables, access the real-time dashboard by navigating to [http://localhost:8501](http://localhost:8501) in your web browser.

# General Dashboard for Premier League

3. This dashboard provides an overview of the Premier League.

   ![General Dashboard](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/first.png)

# Dashboard for Any Team in Premier League

4. **Team Selection**: Select the desired team to view specific insights.

   ![Team Selection](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg1.png)

5. **Team Dashboard**: View detailed information about the team's performance.

   ![Team Dashboard](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg2.png)

6. **Player Statistics**: Analyze player statistics.

   ![Player Statistics](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg3.png)

7. **Match Analysis**: Explore match analysis and historical data.

   ![Match Analysis](https://github.com/2000aliali/Streaming-Premier-League-Champions-Data/blob/main/Images/timg4.png)



