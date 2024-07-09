import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'dataset/ipl_2024_deliveries.csv'
ipl_data = pd.read_csv(file_path)

# Team performance analysis
team_runs = ipl_data.groupby('batting_team')['runs_of_bat'].sum().reset_index()
team_runs = team_runs.rename(columns={'runs_of_bat': 'total_runs'})

wickets = ipl_data[ipl_data['player_dismissed'].notna()]
team_wickets = wickets.groupby('bowling_team')['player_dismissed'].count().reset_index()
team_wickets = team_wickets.rename(columns={'player_dismissed': 'total_wickets'})

team_performance = pd.merge(team_runs, team_wickets, left_on='batting_team', right_on='bowling_team')
team_performance = team_performance.drop('bowling_team', axis=1)

# Player performance analysis
batsman_performance = ipl_data.groupby('striker')['runs_of_bat'].sum().reset_index()
batsman_performance = batsman_performance.rename(columns={'runs_of_bat': 'total_runs'})
top_batsmen = batsman_performance.sort_values(by='total_runs', ascending=False).head(10)

bowler_performance = ipl_data[ipl_data['player_dismissed'].notna()]
bowler_performance = bowler_performance.groupby('bowler')['player_dismissed'].count().reset_index()
bowler_performance = bowler_performance.rename(columns={'player_dismissed': 'total_wickets'})
top_bowlers = bowler_performance.sort_values(by='total_wickets', ascending=False).head(10)

# Venue performance analysis
venue_performance_runs = ipl_data.groupby('venue')['runs_of_bat'].sum().reset_index()
venue_performance_runs = venue_performance_runs.rename(columns={'runs_of_bat': 'total_runs'})

venue_performance_wickets = ipl_data[ipl_data['player_dismissed'].notna()]
venue_performance_wickets = venue_performance_wickets.groupby('venue')['player_dismissed'].count().reset_index()
venue_performance_wickets = venue_performance_wickets.rename(columns={'player_dismissed': 'total_wickets'})

venue_performance = pd.merge(venue_performance_runs, venue_performance_wickets, on='venue')

# Streamlit UI
st.set_page_config(page_title="IPL 2024 Analysis", layout="wide")

st.title("IPL 2024 Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_team = st.sidebar.selectbox("Select Team", options=team_performance['batting_team'].unique())
selected_venue = st.sidebar.selectbox("Select Venue", options=venue_performance['venue'].unique())

st.sidebar.markdown("### Top Performers")
top_batsmen_limit = st.sidebar.slider("Number of Top Batsmen", min_value=5, max_value=20, value=10)
top_bowlers_limit = st.sidebar.slider("Number of Top Bowlers", min_value=5, max_value=20, value=10)

# Filtered Data
filtered_team_performance = team_performance[team_performance['batting_team'] == selected_team]
filtered_venue_performance = venue_performance[venue_performance['venue'] == selected_venue]
top_batsmen_filtered = top_batsmen.head(top_batsmen_limit)
top_bowlers_filtered = top_bowlers.head(top_bowlers_limit)

# Main Layout
st.header("Team Performance")
st.dataframe(filtered_team_performance)

st.header("Venue Performance")
st.dataframe(filtered_venue_performance)

st.header("Top Performers")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Batsmen")
    st.dataframe(top_batsmen_filtered)
with col2:
    st.subheader("Top Bowlers")
    st.dataframe(top_bowlers_filtered)

# Visualizations
st.header("Visualizations")

st.subheader("Total Runs by Teams")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(filtered_team_performance['batting_team'], filtered_team_performance['total_runs'], color='skyblue')
ax.set_xlabel('Total Runs')
ax.set_ylabel('Team')
ax.set_title('Total Runs by Teams in IPL 2024')
st.pyplot(fig)

st.subheader("Top Batsmen")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_batsmen_filtered['striker'], top_batsmen_filtered['total_runs'], color='lightcoral')
ax.set_xlabel('Total Runs')
ax.set_ylabel('Batsman')
ax.set_title('Top Batsmen in IPL 2024')
st.pyplot(fig)

st.subheader("Top Bowlers")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(top_bowlers_filtered['bowler'], top_bowlers_filtered['total_wickets'], color='seagreen')
ax.set_xlabel('Total Wickets')
ax.set_ylabel('Bowler')
ax.set_title('Top Bowlers in IPL 2024')
st.pyplot(fig)

st.subheader("Total Runs by Venue")
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(filtered_venue_performance['venue'], filtered_venue_performance['total_runs'], color='lightblue')
ax.set_xlabel('Total Runs')
ax.set_ylabel('Venue')
ax.set_title('Total Runs by Venue in IPL 2024')
st.pyplot(fig)

st.subheader("Total Wickets by Venue")
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(filtered_venue_performance['venue'], filtered_venue_performance['total_wickets'], color='salmon')
ax.set_xlabel('Total Wickets')
ax.set_ylabel('Venue')
ax.set_title('Total Wickets by Venue in IPL 2024')
st.pyplot(fig)
