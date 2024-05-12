import streamlit as st
import DataProcess
import altair as alt
import pandas as pd
from scipy.interpolate import interp1d

# ------------------------------------------------------------------------------
# --------------------------------- Main settings ------------------------------
# ------------------------------------------------------------------------------
# Set page configuration options
st.set_page_config(
    layout="wide", 
    page_title="Humidity: MonthlyStatement",
    page_icon="📆",
)

# ------------------------------------------------------------------------------
# --------------------------------- Create data --------------------------------
# ------------------------------------------------------------------------------
# get absolute humidity dataframe
abs_hum, _, _ = DataProcess.GetData()

# get chart data
ChartPropDF=DataProcess.GetChartData()

# melted data for line chart
abs_melted = abs_hum.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity')

# Find the end of each month
month_ends = abs_hum.resample('M').mean().reset_index()

# difference of inside/outside
abs_hum_diff = pd.DataFrame()
for c in range(len(abs_hum.columns)-2):
  abs_hum_diff[abs_hum.columns[c]] = (abs_hum[abs_hum.columns[c]]-abs_hum[abs_hum.columns[len(abs_hum.columns)-1]])

# ------------------------------------------------------------------------------
# -------------------------------- Create charts -------------------------------
# ------------------------------------------------------------------------------

abs_hum_by_month = abs_hum
abs_hum_diff_by_month = abs_hum_diff

# create columns
colA, colB, colC = st.columns([0.30,0.6,0.30])

with colB:

    # ---------------------------------
    # description
    st.markdown('# 📆MonthlyStatement')
    st.markdown('---')
    st.markdown('### Monthly Charts:')
    st.markdown('At this point, we can better understand our data, in monthly resolution. On higher steps the data is distorted, because of the different amount of monthly data. We can analyze on two charts, the absolute humidity on the left, and the difference of this value compared to themeasurement outside on the right.')

    # create selectbox
    select_options = set([f"{date.year}.{str(date.month).zfill(2)}" for date in abs_hum.index])
    select_options = list(select_options)
    select_options.append('None')
    select_options=sorted(select_options)
    select_options = [select_options[-1]]+select_options[:-1]
    selected_period = st.selectbox("Period", select_options)    

    # create data by selected month, or whole datase if None
    if selected_period !='None':
        selected_year, selected_month = map(int, selected_period.split('.'))
        abs_hum_by_month = abs_hum[(abs_hum.index.year == selected_year) & (abs_hum.index.month == selected_month)]
        abs_hum_diff_by_month = abs_hum_diff[(abs_hum_diff.index.year == selected_year) & (abs_hum_diff.index.month == selected_month)]

        abs_hum_by_month_melted = abs_hum_by_month.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity')
        abs_hum_diff_by_month_melted = abs_hum_diff_by_month.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity Difference')

    else:
        abs_hum_by_month_melted = abs_hum.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity')
        abs_hum_diff_by_month_melted = abs_hum_diff.reset_index().melt(id_vars=['datetime'], var_name='Location', value_name='Absolute Humidity Difference')

    # ---------------------------------
    # Altair line chart absolute humidity
    line_chart_by_month = alt.Chart(abs_hum_by_month_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=True)),
        y=alt.Y('Absolute Humidity:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    ).properties(
        title='Absolute Humidity:'
    )

    # ---------------------------------
    # Altair line chart absolute humidity difference
    line_chart_by_month_diff = alt.Chart(abs_hum_diff_by_month_melted).mark_line().encode(
        x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=True)),
        y=alt.Y('Absolute Humidity Difference:Q', axis=alt.Axis(grid=True)),
        color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=None)
    ).properties(
        title='Absolute Humidity Difference:'
    )
   
    # ---------------------------------
    # Altair boxplot chart, absolute humidity by location
    boxplot_abs_hum = alt.Chart(abs_hum_by_month_melted).mark_boxplot().encode(
    x=alt.X('Location:N', sort=list(abs_hum.columns), axis=alt.Axis(grid=False)),
    y=alt.Y('Absolute Humidity:Q', axis=alt.Axis(grid=True)),
    color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=list(abs_hum.columns))
    ).configure_view(
        stroke='transparent',
        fill=ChartPropDF.loc[1,'BGColor']
    ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
    )

    # ---------------------------------
    # Altair boxplot chart, absolute humidity difference by location
    boxplot_abs_hum_diff = alt.Chart(abs_hum_diff_by_month_melted).mark_boxplot().encode(
    x=alt.X('Location:N', sort=list(abs_hum.columns), axis=alt.Axis(grid=False)),
    y=alt.Y('Absolute Humidity Difference:Q', axis=alt.Axis(grid=True)),
    color=alt.Color('Location:N', scale=alt.Scale(range=ChartPropDF.loc[0,'ChartValueColors']),  sort=list(abs_hum.columns))
    ).configure_view(
        stroke='transparent',
        fill=ChartPropDF.loc[1,'BGColor']
    ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
    )

    # ---------------------------------
    # create layer chart, if whole dataset is used add month end
    if selected_period !='None':    
        # create layer chart
        layered_abs_hum = alt.layer(line_chart_by_month).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
        ).interactive()
        # create layer chart
        layered_abs_hum_diff = alt.layer(line_chart_by_month_diff).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
        ).interactive()
    
    else:
        # Find the end of each month
        month_ends = abs_hum.resample('M').mean().reset_index()
        # Create vertical lines for month ends
        month_end_lines_main = alt.Chart(month_ends).mark_rule(color=ChartPropDF.loc[0,'GridColor'] ).encode(
            x=alt.X('datetime:T', axis=alt.Axis(grid=False, labels=False)),
        )
        # create layer chart
        layered_abs_hum = alt.layer(line_chart_by_month+month_end_lines_main).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
        ).interactive()
        # create layer chart
        layered_abs_hum_diff = alt.layer(line_chart_by_month_diff+month_end_lines_main).configure_view(
            stroke='transparent',
            fill=ChartPropDF.loc[0,'BGColor']
        ).configure_axis(
            gridColor=ChartPropDF.loc[0,'GridColor'], 
            gridOpacity=0.5  
        ).interactive()

    # create columns
    col1, col2= st.columns([0.5, 0.5])

    # show charts
    with col1:
        with st.container(border=True):
            st.altair_chart(layered_abs_hum, use_container_width=True)
            st.altair_chart(boxplot_abs_hum, use_container_width=True)
            st.dataframe(abs_hum_by_month.describe().round(decimals=2), use_container_width=True)
    
    with col2:
        with st.container(border=True):
            st.altair_chart(layered_abs_hum_diff, use_container_width=True)
            st.altair_chart(boxplot_abs_hum_diff, use_container_width=True)
            st.dataframe(abs_hum_diff_by_month.describe().round(decimals=2), use_container_width=True)

    # ---------------------------------
    # description
    st.markdown('---')
    st.markdown('# Observations')
    st.markdown('''
It can be seen that there are fluctuations in the humidity outside in the summer months. As long as the temperature is high during the day, there is more moisture in the air, but when it cools down at night, it decreases. The structure also has its own fluctuation, it adjusts to the external parameters, but does not absorb the fluctuations. 
Then we can observe something interesting from autumn. As long as the humidity outside is minimal, the structure does not adapt to it. This is due to the non-100 percent vapor barrier. The evaluation of this will be discussed later. Another interesting observation is that the humidity is relatively lower at the southern measuring point in winter. The pipes from the outside arrive there, which I suspect were not properly sealed and thus the cold dry air can flow in, this is also supported by the temperature data.''')
    