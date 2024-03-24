from kafka import KafkaProducer
import json
import requests
from bs4 import BeautifulSoup
import time



#****************************************************************************************************************** 
import psycopg2

# Correct the connection parameters
connection_properties = {
    "dbname": "premier_league",
    "user": "ali",
    "password": "your password",
    "host": "localhost",
    "port": "5432"
}

table_name = "top_score2"

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
topic_name = 'topic_top_score'

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers=bootstrap_servers,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

url = "https://www.bbc.com/sport/football/premier-league/top-scorers"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
# Find the table containing the Premier League standings
table = soup.find("table", class_="gs-o-table")
ranking = table.find_all("td", class_="gs-o-table__cell")
# Find all rows (players) in the table
rows = table.find_all("td", class_="gs-o-table__cell gs-o-table__cell--left")
i = 0
j = 0
print("************************************************")
player_data = {}
for rr in ranking:
    i = i + 1
    tt = rr.text
    name = tt

    if i == 1:
        rank = tt
        player_data['rank'] = int(name)
        print("ranks is ", name)
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

        # Update data player dictionary
        player_data["player_name"] = player_name
        player_data["team_name"] = team_name

        print("Player Name:", player_name)
        print("Team Name:", team_name)
        j = j + 1
        rank = tt
        print("name  is ", name)
        continue
    if i == 3:
        total_goals = tt
        player_data["total_goals"] = int(total_goals)
        print("total of goal scored  is ", name)
        continue
    if i == 4:
        total_assists = tt
        player_data["total_assists"] = int(total_assists)
        print("total of assists  is ", name)
        continue
    if i == 5:
        total_games_played = tt
        player_data["total_games_played"] = int(total_games_played)
        print("total of games played  is ", name)
        continue
    if i == 6:
        goal_per_90 = tt
        player_data["goal_per_90"] = float(goal_per_90)
        print("goal per 90  is ", name)
        continue
    if i == 7:
        mins_per_goal = tt
        player_data["mins_per_goal"] = int(mins_per_goal)
        print("Mins per Goal  is ", name)
        continue
    if i == 8:
        total_shots = tt
        player_data["total_shots"] = int(total_shots)
        print("total shots is ", name)
        continue
    if i == 9:
        '''goal_conversion = tt
        player_data["goal_conversion"] = int(goal_conversion)
        print("goal conversion   is ", name)
        continue
         '''
        goal_conversion = tt
        goal_conversion_without_percent=tt.strip('%')
        player_data["goal_conversion"] = int(goal_conversion_without_percent)
        print("goal conversion   is ", name)
        continue
        # Example conversion for "24%"

    if i == 10:
        ''''
        shot_accuracy = tt
        player_data["shot_accuracy"] = int(shot_accuracy)
        print("shot accuracy  is ", name)
        i = 0
        print("************************************************")
        '''
        shot_accuracy = tt.strip('%')

        player_data["shot_accuracy"] = int(shot_accuracy)
        print("shot accuracy  is ", name)
        i = 0
        print("************************************************")

        # Send player data to Kafka topic
        producer.send(topic_name, value=player_data)
        print("Message sent to Kafka topic:", player_data)
        time.sleep(10)
        player_data = {}


