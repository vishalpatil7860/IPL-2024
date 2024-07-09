import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

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

# Sidebar configuration
st.set_page_config(page_title="IPL 2024 Analysis", layout="wide")

# Helper function for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

st.title("IPL 2024 Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
selected_team = st.sidebar.selectbox("Select Team", options=team_performance['batting_team'].unique(), index=0)
selected_venue = st.sidebar.selectbox("Select Venue", options=venue_performance['venue'].unique(), index=0)

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
st.dataframe(filtered_team_performance.style.highlight_max(axis=0, color='lightgreen'))

st.header("Venue Performance")
st.dataframe(filtered_venue_performance.style.highlight_max(axis=0, color='lightgreen'))

st.header("Top Performers")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top Batsmen")
    st.dataframe(top_batsmen_filtered.style.highlight_max(axis=0, color='lightgreen'))
with col2:
    st.subheader("Top Bowlers")
    st.dataframe(top_bowlers_filtered.style.highlight_max(axis=0, color='lightgreen'))

# Visualizations
st.header("Visualizations")

# Total Runs by Teams
st.subheader("Total Runs by Teams")
fig = px.bar(team_performance, x='total_runs', y='batting_team', orientation='h', color='total_runs',
             color_continuous_scale='Viridis', title='Total Runs by Teams in IPL 2024')
st.plotly_chart(fig)

# Top Batsmen
st.subheader("Top 10 Batsmen")
fig = px.bar(top_batsmen_filtered, x='total_runs', y='striker', orientation='h', color='total_runs',
             color_continuous_scale='Plasma', title='Top Batsmen in IPL 2024')
st.plotly_chart(fig)

# Top Bowlers
st.subheader("Top 10 Bowlers")
fig = px.bar(top_bowlers_filtered, x='total_wickets', y='bowler', orientation='h', color='total_wickets',
             color_continuous_scale='Magma', title='Top Bowlers in IPL 2024')
st.plotly_chart(fig)

# Total Runs by Venue
st.subheader("Total Runs by Venue")
fig = px.bar(venue_performance, x='total_runs', y='venue', orientation='h', color='total_runs',
             color_continuous_scale='Viridis', title='Total Runs by Venue in IPL 2024')
st.plotly_chart(fig)

# Total Wickets by Venue
st.subheader("Total Wickets by Venue")
fig = px.bar(venue_performance, x='total_wickets', y='venue', orientation='h', color='total_wickets',
             color_continuous_scale='Cividis', title='Total Wickets by Venue in IPL 2024')
st.plotly_chart(fig)