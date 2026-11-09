# This creates the page for displaying data visualizations.

import streamlit as st
import json 
import os
import pandas as pd 
import plotly.express as px 

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Anime Data Visuals")


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---

with open("data.json") as jsonfile: 
    death_note = json.load(jsonfile) 
d_n_table = pd.DataFrame(death_note["data_points"]) 

st.subheader(death_note["chart_title"]) 
st.write("IMDb Ratings for Death Note") 
st.header("Ratings Across the Whole Series") 

chart_of_eps = px.line(
    d_n_table, x="episode", y = "value", hover_name = "label", markers = True,
    title = "IMDb Rating by Episode",
    labels = {"episode": "Episode Number", "value": "IMDb Rating (out of 10)"})

st.plotly_chart(chart_of_eps) 
st.header("Explore a Range of Episodes") 
first_episode = int(d_n_table["episode"].min()) 
last_episode = int(d_n_table["episode"].max()) 

st.slider("Choose an episode range: did the ratings go down after L's death?", first_episode, last_episode,(first_episode, last_episode), key = "ep_range")
start,stop = st.session_state.ep_range

chosen = d_n_table[(d_n_table["episode"] >= start) & (d_n_table["episode"] <= stop )]

chart_of_chosen = px.bar(
    chosen, x="episode", y="value", hover_name="label",
    title=f"IMDb Ratings for Episodes {start}–{stop}",
    labels={"episode": "Episode Number", "value": "IMDb Rating (out of 10)"})
st.plotly_chart(chart_of_chosen) 

st.write(f"Average rating for this range: **{chosen['value'].mean():.2f}/10**")

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
st.header("Anime Genre and Hours Results")
if os.path.exists("data.csv") and os.path.getsize("data.csv")>0:
    survey = pd.read_csv("data.csv")
    average = survey.groupby("Category")["Value"].mean().reset_index()
    chart_of_avg = px.bar(average, x="Category", y = "Value",
    title = "Favorite genre and average weekly hours watched",
    labels = {"Category": "Favorite Genre", "Value": "Average hours per week"})
    st.plotly_chart(chart_of_avg)

    genres = list(survey["Category"].unique())
    st.multiselect("Compare genres:", genres, default=genres, key="genre_picked")
    picked = survey[survey["Category"].isin(st.session_state.genre_picked)]
    count = picked["Category"].value_counts().reset_index()

    piechart = px.pie(count, names = "Category", values = "count", title = "Pie Chart of Anime Genres and Hours Watched",labels = {"Category": "Favorite Genre", "count": "Number of People"})
    st.plotly_chart(piechart)

    mean = picked["Value"].mean()
    median = picked["Value"].median()

    if "old_mean" not in st.session_state:
        st.session_state.old_mean = mean
    if "old_median" not in st.session_state:
        st.session_state.old_median = median
    st.metric("Mean hours per week", f"{mean:.2f}", delta = f"{mean-st.session_state.old_mean:.2f}")
    st.metric("Median hours per week", f"{median:.2f}", delta = f"{median-st.session_state.old_median:.2f}")
    st.session_state.old_mean = mean
    st.session_state.old_median = median 

else:
    st.warning("No response yet!")




