
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pptx import Presentation
from io import BytesIO

# Load data
csv_path = "game_portfolio_extended.csv"
df = pd.read_csv(csv_path)

# Load PowerPoint
ppt_path = "game_portfolio_analysis.pptx"
ppt = Presentation(ppt_path)

# Load the CSV file
file_path = 'games_data.csv'
games_data = pd.read_csv(file_path)

# Custom CSS to hide the Streamlit menu and footer
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)



# Set up the sidebar for category selection
st.sidebar.title("Game Categories")
category = st.sidebar.radio("Select a category", games_data['Category'].unique())

# Set up the sidebar for column selection
st.sidebar.title("Display Options")
all_columns = games_data.columns.tolist()
selected_columns = st.sidebar.multiselect("Select columns to display", all_columns, default=all_columns)

# Filter the data based on the selected category and columns
filtered_data = games_data[games_data['Category'] == category][selected_columns]

# Display the filtered dataframe
st.title("Games Data")
st.write(f"Displaying games in the category: {category}")
st.dataframe(filtered_data)



# Sidebar options
quadrant_options = df['Quadrant'].unique()
selected_quadrant = st.sidebar.multiselect('Select Quadrant', quadrant_options, default=quadrant_options)

# Filter data
filtered_df = df[df['Quadrant'].isin(selected_quadrant)]

# Display data
st.title("Game Portfolio Analysis")
st.write("## Filtered Data")
st.dataframe(filtered_df)

# Display charts
st.write("## Engagement Charts")
def create_engagement_chart(df, metric):
    engagement_data = df.groupby("Quadrant")[metric].value_counts(normalize=True).unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(10, 6))
    engagement_data.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title(f"{metric} by Quadrant")
    ax.set_xlabel("Quadrant")
    ax.set_ylabel("Proportion")
    st.pyplot(fig)

create_engagement_chart(filtered_df, "Mobile Engagement")
create_engagement_chart(filtered_df, "PC Engagement")
create_engagement_chart(filtered_df, "Console Engagement")

# Display monetization trends chart
st.write("## Monetization Trends")
monetization_data = filtered_df.groupby("Quadrant")["Monetization Model"].value_counts(normalize=True).unstack().fillna(0)
fig, ax = plt.subplots(figsize=(10, 6))
monetization_data.plot(kind='bar', stacked=True, ax=ax)
ax.set_title("Monetization Models by Quadrant")
ax.set_xlabel("Quadrant")
ax.set_ylabel("Proportion")
st.pyplot(fig)

# Display PowerPoint
st.write("## PowerPoint Presentation")
ppt_buffer = BytesIO()
ppt.save(ppt_buffer)
ppt_buffer.seek(0)
st.download_button("Download PowerPoint", ppt_buffer, file_name="game_portfolio_analysis.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")
st.title("Game Cultural Fit Analysis")
st.image("picgt.PNG")

st.info("v1.2- 6-27 dw")