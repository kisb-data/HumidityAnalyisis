import streamlit as st
import DataProcess
import altair as alt
import pandas as pd
import numpy as np

# ------------------------------------------------------------------------------
# --------------------------------- Main settings ------------------------------
# ------------------------------------------------------------------------------
# Set page configuration options
st.set_page_config(
    layout="wide", 
    page_title="Humidity: CheckTheDewPoint",
    page_icon="👉",
)

# ------------------------------------------------------------------------------
# --------------------------------- Create data --------------------------------
# ------------------------------------------------------------------------------

# Function to calculate dew point
def dew_point(temperature, humidity):
    a = 17.271
    b = 237.7
    alpha = ((a * temperature) / (b + temperature)) + np.log(humidity / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return dew_point

# get absolute humidity dataframe
_, rel_hum, temp = DataProcess.GetData()

# get chart data
ChartPropDF=DataProcess.GetChartData()

# Calculate dew point for each cell in the DataFrame
dew_point_data = {}
for c in range(len(rel_hum.columns)):
    dew_point_data[str(temp.columns[c])[:-2]] = dew_point(temp[temp.columns[c]], rel_hum[rel_hum.columns[c]])

# Create DataFrame for dew point
dew_point_df = pd.DataFrame(dew_point_data, index=rel_hum.index)

hum_diff = pd.DataFrame()

for c in range(len(dew_point_df.columns)):
    hum_diff[dew_point_df.columns[c]] = temp[temp.columns[c]]-dew_point_df[dew_point_df.columns[c]]

# ------------------------------------------------------------------------------
# -------------------------------- Create charts -------------------------------
# ------------------------------------------------------------------------------

# create columns
colA, colB, colC = st.columns([0.30,0.6,0.30])

with colB:

    # ---------------------------------
    # description
    st.markdown('# 👉CheckTheDewPoint')
    st.markdown('---')
    st.markdown('''The most important point is here, to see how many degrees the temperature needs to drop for the vapor to condense.''')

    # create selectbox
    select_options = set([f"{date.year}.{str(date.month).zfill(2)}" for date in hum_diff.index])
    select_options = list(select_options)
    select_options.append('None')
    select_options=sorted(select_options)
    select_options = [select_options[-1]]+select_options[:-1]
    selected_period = st.selectbox("Period", select_options)    

    # create data by selected month, or whole datase if None
    if selected_period !='None':
        selected_year, selected_month = map(int, selected_period.split('.'))
        hum_diff = hum_diff[(hum_diff.index.year == selected_year) & (hum_diff.index.month == selected_month)]

    # Reshape data using melt
    df_melted =hum_diff.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Temperature')

    # Create line chart using Altair
    line_chart = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False)),
        y=alt.Y('Temperature:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    ).properties(
        title='Temperature to dew point:',     
    ).configure_view(
        stroke='transparent',
        fill=ChartPropDF.loc[0,'BGColor']
    ).configure_axis(
        gridColor=ChartPropDF.loc[0,'GridColor'], 
        gridOpacity=0.5  
    ).interactive()

    # Display the chart using Streamlit
    st.altair_chart(line_chart, use_container_width=True)

    # ---------------------------------
    # description
    st.markdown('---')
    st.markdown('# Observations')
    st.markdown('''''')