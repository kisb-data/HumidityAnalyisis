import streamlit as st
import DataProcess
import altair as alt
import pandas as pd 

# ------------------------------------------------------------------------------
# --------------------------------- Main settings ------------------------------
# ------------------------------------------------------------------------------
# Set page configuration options
st.set_page_config(
    layout="wide", 
    page_title="Humidity: ExploreData",
    page_icon="📈",
)

# ------------------------------------------------------------------------------
# --------------------------------- Create data --------------------------------
# ------------------------------------------------------------------------------
# get absolute humidity dataframe
abs_hum, rel_hum, temp = DataProcess.GetData()

# get chart data
ChartPropDF=DataProcess.GetChartData()

# melted data for line chart
abs_melted = abs_hum.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity')
rel_melted = rel_hum.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Relative Humidity')
temp_melted = temp.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Temperature')

# Find the end of each month
month_ends = abs_hum.resample('M').mean().reset_index()

# ------------------------------------------------------------------------------
# -------------------------------- Create charts -------------------------------
# ------------------------------------------------------------------------------

# create columns
colA, colB, colC = st.columns([0.30,0.6,0.30])

with colB:

    # ---------------------------------
    # description
    st.markdown('# ✏️ExploreData')
    st.markdown('---')
    st.markdown('### All data:')
    st.markdown('''Here we can see our 3 main parameters, temperature, absolute and relative humidity. I measured the data on the four sides of the house at 30 cm from the base and one place under the slab and for comparison one place outside. The data was collected manually at random times.''')

    # ---------------------------------
    # Altair line chart absolute humidity
    line_chart_abs = alt.Chart(abs_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=True)),
        y=alt.Y('Absolute Humidity:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    )

    # Altair line chart relative humidity
    line_chart_rel = alt.Chart(rel_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=True)),
        y=alt.Y('Relative Humidity:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    )

    # Altair line chart temperature
    line_chart_temp = alt.Chart(temp_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=True)),
        y=alt.Y('Temperature:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    )

    # Create vertical lines for month ends
    month_end_lines_main = alt.Chart(month_ends).mark_rule(color=ChartPropDF.loc[0,'GridColor'] ).encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=False)),
    )
    
    # create chart tabs
    tab1, tab2, tab3 = st.tabs(["Absolute humidity", "Relative humidity", "Temperature"])
                
    # add tab1
    with tab1:
        # create layer chart
        layered_main = alt.layer(line_chart_abs+month_end_lines_main).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
        ).interactive()

        # show chart
        st.altair_chart(layered_main, use_container_width=True)

        # description
        st.markdown('---')
        st.markdown('## Description: ')
                   
        st.dataframe(abs_hum.describe().round(decimals=2), use_container_width=True)

    # add tab2
    with tab2:
        # create layer chart
        layered_main = alt.layer(line_chart_rel+month_end_lines_main).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).interactive()

        # show chart
        st.altair_chart(layered_main, use_container_width=True)

        # description
        st.markdown('---')
        st.markdown('## Description: ')
    
        st.dataframe(rel_hum.describe().round(decimals=0), use_container_width=True)

    # add tab3
    with tab3:
        # create layer chart
        layered_main = alt.layer(line_chart_temp+month_end_lines_main).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).interactive()

        # show chart
        st.altair_chart(layered_main, use_container_width=True)

        # description
        st.markdown('---')
        st.markdown('## Description: ')
     
        st.dataframe(temp.describe().round(decimals=0), use_container_width=True)

    # ---------------------------------
    # Grouping data by month and counting observes
    monthly_counts = abs_hum.resample('M').size().reset_index(name='Count')
   
    # Creating Altair bar chart
    chart = alt.Chart(monthly_counts).mark_bar(color=ChartPropDF.loc[2,'ChartValueColors'][0], size=40).encode(
        x=alt.X('datetime:T', title='Month', axis=alt.Axis(grid=False)),
        y=alt.Y('Count:Q', title='Number of Events', axis=alt.Axis(grid=True)),
    ).configure_view(
        stroke='transparent',
        fill=ChartPropDF.loc[2,'BGColor']
    ).configure_axis(
        gridColor=ChartPropDF.loc[2,'GridColor'], 
        gridOpacity=0.5  
    ).interactive()
    
    monthly_counts['datetime'] = monthly_counts['datetime'] - pd.DateOffset(months=1)

    st.text("")
    st.altair_chart(chart, use_container_width=True)

    # ---------------------------------
    # description
    st.markdown('---')
    st.markdown('# Observations')
    st.markdown(''' As you can see, relative humidity is not really suitable for comparing data, so we will use absolute humidity in the future. The description contains a lot of interesting things, but don't jump to conclusions yet. As you can see, the frequency of the data is not the same every month, which distorts the evaluation. However, what can already be clearly seen is that there is a difference between the winter and summer data, but we will evaluate this later.''')
