print("before")

from kafka import KafkaProducer
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import psycopg2

# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'topic_premier_league'
connection_properties = {
    "dbname": "premier_league",
    "user": "ali",
    "password": "123456789",
    "host": "localhost",
    "port": "5432"
}

table_name = "final_table"

def drop_table(table_name, connection_properties):
    try:
        # Establish connection using the correct parameters
        conn = psycopg2.connect(**connection_properties)
        print("Connected to the database")

        # Drop table query
        drop_query = f"DROP TABLE IF EXISTS {table_name};"

        # Create a cursor
        cursor = conn.cursor()

        # Execute the query
        cursor.execute(drop_query)

        # Commit the transaction
        conn.commit()

        print(f"Table '{table_name}' dropped successfully.")

    except Exception as e:
        print(f"Error: {e}")
        exit(10)

# Call the function with corrected parameters
drop_table(table_name, connection_properties)
#********************************************************************

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# URL to scrape data from
url = "https://www.bbc.com/sport/football/premier-league/table"

# Extract data from the website
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

table = soup.find("table", class_="ssrcss-14j0ip6-Table e3bga5w5")
rows = table.find_all("tr", class_="ssrcss-usj84m-TableRow e3bga5w3")

f = table.find_all("tr", class_="ssrcss-196x9m3-TableRow e3bga5w3")
# Data container
#data = []

# Extracting data from rows
for row in rows:
    message = {}

    rank = int(row.find_all("td", class_="ssrcss-1b9osum-TableCell e3bga5w2")[0].text)
    team_name = str(row.find("div", class_="ssrcss-3u4qof-Team e1uquauq6").text)
    games_played = int(row.find_all("td", class_="ssrcss-1b9osum-TableCell e3bga5w2")[2].text)
    games_won = int(row.find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[0].text)
    games_drawn = int(row.find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[1].text)
    games_lost = int(row.find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[2].text)
    goals_scored = int(row.find_all("td", class_="ssrcss-6pzgq-TableCell e3bga5w2")[0].text)
    goals_conceded = int(row.find_all("td", class_="ssrcss-6pzgq-TableCell e3bga5w2")[1].text)
    points = int(row.find("span", class_="ssrcss-du60gv-Points e1uquauq3").text)

    message = {
        'Rank': rank,
        'Team Name': team_name,
        'Games Played': games_played,
        'Games Won': games_won,
        'Games Drawn': games_drawn,
        'Games Lost': games_lost,
        'Goals Scored': goals_scored,
        'Goals Conceded': goals_conceded,
        'Points': points
    }

    # Append data to the list
    #data.append(message)
    #print(message)
    # Check for data change
    producer.send(topic_name, value=message)
    print("Message sent to Kafka topic:", message)

# Update prev_data

# Sleep for 1 minute before fetching data again
    time.sleep(10)
for i in range(0,3):

    new_row={}
    rank = int(f[i].find("td", class_="ssrcss-1b9osum-TableCell e3bga5w2").text)
    team_name = str(f[i].find("div", class_="ssrcss-3u4qof-Team e1uquauq6").text)
    games_played =  int(f[i].find_all("td", class_="ssrcss-1b9osum-TableCell e3bga5w2")[2].text)
    games_winn = int(f[i].find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[0].text)
    games_drawn = int(f[i].find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[1].text)
    games_lost = int(f[i].find_all("td", class_="ssrcss-45ku6m-TableCell e3bga5w2")[2].text)
    goals_scored = int(f[i].find_all("td", class_="ssrcss-6pzgq-TableCell e3bga5w2")[0].text)
    goals_conceded = int(f[i].find_all("td", class_="ssrcss-6pzgq-TableCell e3bga5w2")[1].text)
    points = int(f[i].find("span", class_="ssrcss-du60gv-Points e1uquauq3").text)
    new_row = {'Rank': rank,
                  'Team Name': team_name,
                  'Games Played': games_played,
                  'Games Won': games_winn,
                  'Games Drawn': games_drawn,
                  'Games Lost': games_lost,
                  'Goals Scored': goals_scored,
                  'Goals Conceded': goals_conceded,
                  'Points': points}
    #data.append(new_row)
    #print(new_row)
    # Check for data change
    producer.send(topic_name, value=new_row)
    print("Message sent to Kafka topic:", new_row)
    time.sleep(10)
