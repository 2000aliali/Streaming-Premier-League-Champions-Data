from kafka import KafkaProducer
import json
import requests
from bs4 import BeautifulSoup
import  time




#****************************************************************************************************************** 
import psycopg2

# Correct the connection parameters
connection_properties = {
    "dbname": "premier_league",
    "user": "ali",
    "password": "123456789",
    "host": "localhost",
    "port": "5432"
}

table_name = "top_assists"

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
#*******************************************************************
# Kafka configuration
bootstrap_servers = 'localhost:9092'
topic_name = 'topic_assists'

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

url = "https://www.bbc.com/sport/football/premier-league/top-scorers/assists"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
# Find the table containing the Premier League standings
table = soup.find("table", class_="gs-o-table")
ranking = table.find_all("td", class_="gs-o-table__cell")
# Find all rows (players) in the table
rows = table.find_all("td", class_="gs-o-table__cell gs-o-table__cell--left")
j = 0
i = 0
player_data = {}
print("************************************************")
for rr in ranking:
    # player_data = {}

    i = i + 1
    tt = rr.text
    name = tt
    if i == 1:
        rank = tt
        print("ranks is ", name)
        player_data['rank'] = int(name)

        continue
    if i == 2:
        soup1 = rows[j]
        player_name_element = soup1.find('span', class_='gs-u-vh gs-u-display-inherit@l')

        # Extract the player name
        player_name = player_name_element.text.strip()

        # Find the team name element
        team_name_element = soup1.find('span', class_='gs-u-vh gs-u-display-inherit@m')

        # Extract the team name
        team_name = team_name_element.text.strip()

        print("Player Name:", player_name)
        print("Team Name:", team_name)
        j = j + 1
        rank = tt
        print("name  is ", name)

        player_data['player_name'] = player_name
        player_data['team_name'] = team_name
        continue
    if i == 3:
        total_assists = tt
        print("total of assist  is ", name)
        player_data['total_assists'] = int(total_assists)
        continue
    if i == 4:
        total_goals = tt
        print("total of goal  is ", name)
        player_data['total_goals'] = int(total_goals)
        continue
    if i == 5:
        total_games_played = tt
        print("total of games played  is ", name)
        player_data['total_games_played'] = int(total_games_played)
        continue
    if i == 6:
        chance_created = tt
        print("chance created  is ", name)
        player_data['chance_created'] = int(chance_created)
        continue
    if i == 7:
        chance_per_90 = tt
        print("chance per 90 is ", name)
        player_data['chance_per_90'] = float(chance_per_90)
        continue
    if i == 8:
        total_passes = tt
        print("total passes is ", name)
        player_data['total_passes'] = int(total_passes)
        continue
    if i == 9:
        passes_completed = tt
        print("passes completed is ", name)
        player_data['passes_completed'] = int(passes_completed)
        continue
    if i == 10:
        passes_incompleted = tt
        print("passes incompleted is ", name)
        player_data['passes_incompleted'] = int(passes_incompleted)
        continue
    if i == 11:
        pass_accuracy = tt.strip('%')
        print("pass accuracy is ", name)
        player_data['pass_accuracy'] = int(pass_accuracy)
        i = 0
        print("************************************************")

        # Send player data to Kafka topic
        producer.send(topic_name, value=player_data)
        time.sleep(10)

        print("Message sent to Kafka topic:", player_data)
        player_data = {}
