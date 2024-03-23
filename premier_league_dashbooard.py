import streamlit as st
import psycopg2
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Connection properties
connection_properties = {
    "dbname": "premier_league",
    "user": "ali",
    "password": "123456789",
    "host": "localhost",
    "port": "5432"
}

# Function to fetch data from the database
def fetch_data(query):
    conn = psycopg2.connect(**connection_properties)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# Function to calculate total goals
def calculate_total_goals(df):
    total_goals_all_teams = df['total_goals'].sum()
    return total_goals_all_teams

# Function to create pie chart
def create_pie_chart(df, total_goals_all_teams):
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(df['total_goals'], labels=df['team_name'], autopct='%1.1f%%', startangle=140)
    ax.set_title('Distribution of Total Goals by Team\nTotal Goals: {}'.format(total_goals_all_teams))
    st.pyplot(fig)

def main():
    st.title('Premier League Dashboard')

    # Header to select dashboard type
    dashboard_type = st.selectbox("Select Dashboard", ["General Dashboard", "Team Dashboard"])

    if dashboard_type == "General Dashboard":
        # Fetching and displaying the main table
        query_all = "SELECT * FROM final_table"
        all_teams_data = fetch_data(query_all)
        df = pd.DataFrame(all_teams_data,
                          columns=["Rank", "Team Name", "Games Played", "Games Won", "Games Drawn", "Games Lost",
                                   "Goals Scored", "Goals Conceded", "Points"])
        df = df.set_index('Rank')
        df = df.sort_values(by='Rank')

        # Display the team standings table
        st.subheader('Premier League Standings')
        st.dataframe(df.style.set_properties(**{'text-align': 'center'}).set_table_styles(
            [dict(selector='th', props=[('text-align', 'center')])]))

        # Layout: Two rows, two columns
        col1, col2 = st.columns(2)

        # Fetching and displaying points comparison graph
        query_points = "SELECT \"Team Name\", \"Points\" FROM final_table"
        points_data = fetch_data(query_points)
        df_points = pd.DataFrame(points_data, columns=["Team Name", "Points"])

        # Top left: Points Comparison
        with col1:
            st.subheader('Points Comparison')
            fig_points = px.bar(df_points, x='Team Name', y='Points', title='Premier League Standings',
                                labels={'Team Name': 'Team', 'Points': 'Points'})
            st.plotly_chart(fig_points, use_container_width=True)

        # Fetching and displaying games outcome graph
        query_outcome = "SELECT * FROM final_table"
        outcome_data = fetch_data(query_outcome)
        df_outcome = pd.DataFrame(outcome_data,
                                  columns=["Rank", "Team Name", "Games Played", "Games Won", "Games Drawn",
                                           "Games Lost",
                                           "Goals Scored", "Goals Conceded", "Points"])

        fig_outcome = px.bar(df_outcome, x="Team Name", y=["Games Won", "Games Drawn", "Games Lost"],
                             title="Games Outcome per Team",
                             labels={"value": "Number of Games", "variable": "Outcome", "Team Name": "Team"},
                             color_discrete_map={"Games Won": "green", "Games Drawn": "orange",
                                                  "Games Lost": "red"},
                             barmode="stack")

        # Top right: Games Outcome
        with col2:
            st.subheader('Games Outcome per Team')
            st.plotly_chart(fig_outcome, use_container_width=True)

        # Fetching and displaying total goals distribution pie chart
        query_goals = "SELECT team_name, SUM(total_goals) AS total_goals FROM top_score2 GROUP BY team_name;"
        goals_data = fetch_data(query_goals)
        df_goals = pd.DataFrame(goals_data, columns=["team_name", "total_goals"])
        total_goals_all_teams = calculate_total_goals(df_goals)

        # Bottom left: Total Goals Distribution
        with col1:
            st.subheader('Total Goals Distribution by Team')
            create_pie_chart(df_goals, total_goals_all_teams)

        # Fetching the top 3 scorers in the Premier League
        query_top_scorers = "SELECT * FROM top_score2 ORDER BY total_goals DESC LIMIT 3"
        top_scorers_data = fetch_data(query_top_scorers)
        top_scorers_df = pd.DataFrame(top_scorers_data, columns=["Rank", "Player Name", "Team Name", "Total Goals",
                                                                 "Total Assists", "Games Played", "Goal Per 90",
                                                                 "Mins Per Goal", "Total Shots", "Goal Conversion",
                                                                 "Shot Accuracy"])
        st.subheader('Top Scores for in the Premier League  ')
        st.write(top_scorers_df )

        # Fetching the top 3 assisters in the Premier League
        query_top_assisters = "SELECT * FROM top_assists ORDER BY total_assists DESC LIMIT 3"
        top_assisters_data = fetch_data(query_top_assisters)
        top_assisters_df = pd.DataFrame(top_assisters_data,
                                        columns=["Rank", "Player Name", "Team Name", "Total Assists",
                                                 "Total Goals", "Games Played", "Chance Created",
                                                 "Chance Per 90", "Total Passes", "Goal Incompleted",
                                                 "Pass Accuracy"])
        st.subheader('Top Assists for in the Premier League  ')
        st.write(top_assisters_df )
        # Combining top scorers and top assisters data
        top_players_df = pd.concat([top_scorers_df, top_assisters_df])

        # Calculating combined goals and assists
        top_players_df['Total Goals + Assists'] = top_players_df['Total Goals'] + top_players_df['Total Assists']

        # Sorting by combined goals and assists
        top_players_df = top_players_df.sort_values(by='Total Goals + Assists', ascending=False).head(3)

        # Displaying top players with combined goals and assists
        st.subheader('Top Players with Combined Goals and Assists')
        st.write(top_players_df)


    elif dashboard_type == "Team Dashboard":
        #st.title('Premier League Dashboard')

        # Fetching team names from the database
        query_teams = 'SELECT DISTINCT "Team Name" FROM final_table'
        teams = fetch_data(query_teams)
        team_names = [team[0] for team in teams]

        # Dropdown to select a team
        selected_team = st.selectbox('Select a team:', team_names)

        # Fetching team statistics from the database
        query_team_stats = f"SELECT * FROM final_table WHERE \"Team Name\" = '{selected_team}'"
        team_stats = fetch_data(query_team_stats)

        # Displaying team statistics
        st.subheader('Team Statistics')
        stats_df = pd.DataFrame(team_stats,
                                columns=["Rank", "Team Name", "Games Played", "Games Won", "Games Drawn", "Games Lost",
                                         "Goals Scored", "Goals Conceded", "Points"])
        st.write(stats_df)

        # Fetching data for comparison graph
        query_all = "SELECT \"Team Name\", \"Points\" FROM final_table"
        all_teams_data = fetch_data(query_all)
        df = pd.DataFrame(all_teams_data, columns=["Team Name", "Points"])

        # Creating comparison graph
        query_team_data = f"SELECT \"Goals Scored\", \"Goals Conceded\" FROM final_table WHERE \"Team Name\" = '{selected_team}'"
        team_data = fetch_data(query_team_data)
        team_goals_df = pd.DataFrame(team_data, columns=["Goals Scored", "Goals Conceded"])

        # Creating a pie chart for goals scored and conceded
        fig_pie_goals = px.pie(values=[team_goals_df.iloc[0]['Goals Scored'], team_goals_df.iloc[0]['Goals Conceded']],
                               names=['Goals Scored', 'Goals Conceded'],
                               title=f'Goals Scored and Conceded for {selected_team}',
                               labels={'label': 'Outcome', 'value': 'Number of Goals'})
        st.plotly_chart(fig_pie_goals, use_container_width=True)
        ''''
        st.subheader('Points Comparison')
        fig = px.bar(df, x='Team Name', y='Points', title='Premier League Standings',
                     labels={'Team Name': 'Team', 'Points': 'Points'})
        st.plotly_chart(fig, use_container_width=True)'''

        # Fetching team data for the pie chart
        query_team_data = "SELECT \"Team Name\", \"Games Won\", \"Games Drawn\", \"Games Lost\" FROM final_table"
        team_data = fetch_data(query_team_data)
        team_df = pd.DataFrame(team_data, columns=["Team Name", "Games Won", "Games Drawn", "Games Lost"])

        # Summing up the total number of games won, drawn, and lost for the selected team
        selected_team_data = team_df[team_df['Team Name'] == selected_team]
        total_games = selected_team_data.iloc[0]['Games Won'] + selected_team_data.iloc[0]['Games Drawn'] + \
                      selected_team_data.iloc[0]['Games Lost']

        # Creating a pie chart for wins, draws, and losses distribution
        fig_pie = px.pie(values=[selected_team_data.iloc[0]['Games Won'], selected_team_data.iloc[0]['Games Drawn'],
                                 selected_team_data.iloc[0]['Games Lost']],
                         names=['Games Won', 'Games Drawn', 'Games Lost'],
                         title=f'Wins, Draws, and Losses Distribution for {selected_team}',
                         labels={'label': 'Outcome', 'value': 'Number of Games'})
        st.plotly_chart(fig_pie, use_container_width=True)

        # Fetching top scores for the selected team
        query_top_scores = f"SELECT * FROM top_score2 WHERE \"team_name\" = '{selected_team}' ORDER BY total_goals DESC"
        top_scores_data = fetch_data(query_top_scores)
        top_scores_df = pd.DataFrame(top_scores_data, columns=["Rank", "Player Name", "Team Name", "Total Goals",
                                                               "Total Assists", "Games Played", "Goal Per 90",
                                                               "Mins Per Goal", "Total Shots", "Goal Conversion",
                                                               "Shot Accuracy"])

        # Displaying top scores
        st.subheader(f'Top Scores for {selected_team}')
        st.write(top_scores_df)

        # Fetching top assists for the selected team
        query_top_assists = f"SELECT * FROM top_assists WHERE \"team_name\" = '{selected_team}' ORDER BY total_assists DESC"
        top_assists_data = fetch_data(query_top_assists)
        top_assists_df = pd.DataFrame(top_assists_data, columns=["Rank", "Player Name", "Team Name", "Total Assists",
                                                                 "Total Goals", "Games Played", "Chance Created",
                                                                 "Chance Per 90", "Total Passes", "Goal Incompleted",
                                                                 "Pass Accuracy"])

        # Displaying top assists
        st.subheader(f'Top Assists for {selected_team}')
        st.write(top_assists_df)

        query_team_data = f"SELECT \"Goals Scored\", \"Goals Conceded\" FROM final_table WHERE \"Team Name\" = '{selected_team}'"
        team_data = fetch_data(query_team_data)
        team_goals_df = pd.DataFrame(team_data, columns=["Goals Scored", "Goals Conceded"])

        # Creating a pie chart for goals scored and conceded
        fig_pie_goals = px.pie(values=[team_goals_df.iloc[0]['Goals Scored'], team_goals_df.iloc[0]['Goals Conceded']],
                               names=['Goals Scored', 'Goals Conceded'],
                               title=f'Goals Scored and Conceded for {selected_team}',
                               labels={'label': 'Outcome', 'value': 'Number of Goals'})
        st.plotly_chart(fig_pie_goals, use_container_width=True)


if __name__ == '__main__':
    main()
