# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.selectbox("What's your favorite anime genre?", ["Action", "Mystery", "Romance", "Comedy", "Fantasy", "Horror"])
    value_input = st.text_input("how many hours of anime do you watch per week?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        try:
            hours = float(value_input)
            if hours < 0:
                st.error("Please enter a positive number.")
            else:
                
                new_row = pd.DataFrame({
                    "Category": [category_input],
                    "Value": [hours]
                })

                new_row.to_csv(
                    "data.csv",
                    mode="a",
                    header=not os.path.exists("data.csv") or os.path.getsize("data.csv") == 0,
                    index=False
                )

                st.success("Your responses have been recorded.")
                st.write(f"Favorite genre: {category_input}")
                st.write(f"Hours per week: {hours}")


        except ValueError:
            st.error("Enter a valid number of hours!")

st.divider()
st.header("Current Responses")

if os.path.exists("data.csv") and os.path.getsize("data.csv")>0:
    current_data_df = pd.read_csv("data.csv")
    st.dataframe(current_data_df)
else:
    st.warning("No survey responses.")


      
