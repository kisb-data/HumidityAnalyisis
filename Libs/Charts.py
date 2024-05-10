from colour import Color
import altair as alt
import pandas as pd
import numpy as np

# ---------------------------------
# create charts
def GetChart(data, ChartPropSer):
    
    # ---------------------------------
    # Create color range 
    colors = ChartPropSer.at['ChartValueColors']

    color_range = colors
    rows=len(data)

    if ChartPropSer['ChartType']=="Line":
        rows=len(data.line.unique())

    if ChartPropSer['PaletteType'] == 'Gradient1':
        color_range = [color.hex for color in Color(colors[0]).range_to(Color(colors[1]), rows)]

    elif ChartPropSer['PaletteType'] == 'Gradient2':
        whole = rows
        size1=round(whole*0.7)
        size2=whole-size1+1
        color_range_sub1 = [color.hex for color in Color(colors[0]).range_to(Color(colors[1]), size1)] 
        color_range_sub1.pop()
        color_range_sub2 = [color.hex for color in Color(colors[1]).range_to(Color(colors[2]), size2)] 
        color_range = color_range_sub1+color_range_sub2

    # ---------------------------------
    # Create the Altair bar chart
    if ChartPropSer['ChartType']=="Altair Bar":

        chart = alt.Chart(data).mark_bar().encode(
            x=alt.X('x:O', axis=alt.Axis(grid=True)),
            y=alt.Y('y:Q'),
            color=alt.Color('x:N', scale=alt.Scale(range=color_range))
        ).properties(
            title=ChartPropSer['ChartName']
        ).configure_view(
            fill=ChartPropSer['BGColor'], 
            strokeWidth=0  
        ).configure_axis(
            grid=True,  
            gridColor=ChartPropSer['GridColor'] 
        )

        return chart
            
    # Create the Altair line chart
    if ChartPropSer['ChartType']=="Altair Line":

        chart = alt.Chart(data).mark_line().encode(
            x=alt.X('index', axis=alt.Axis(grid=True)),
            y='value',
            color=alt.Color('line:N', scale=alt.Scale(range=color_range))
        ).properties(
            title=ChartPropSer['ChartName']
        ).configure_view(
            fill=ChartPropSer['BGColor'] 
        ).configure_axis(
            grid=True,  
            gridColor=ChartPropSer['GridColor']  
        )

        return chart

    # Create the Altair heatmap
    if ChartPropSer['ChartType']=="Altair Heatmap":
    
        chart = alt.Chart(data).mark_rect().encode(
            x=alt.X('x:O', axis=alt.Axis(labels=False)),
            y=alt.Y('y:O', axis=alt.Axis(labels=False)),
            color=alt.Color('value', scale=alt.Scale(range=[colors[0], colors[1]]))
        ).properties(
            title=ChartPropSer['ChartName']
        )
        return chart

# ---------------------------------
# generate random chart data  
def GetRandomChartData(type, size):

    data = pd.DataFrame()

    if type=='Altair Bar':
        return pd.DataFrame({'x': range(size), 'y': np.random.randint(3,10, size=size)})

    if type=='Altair Line':
        for i in range(size):
            data[f'line_{i+1}'] = np.random.randint(1, 10, 10)

        return data.reset_index().melt(id_vars='index', var_name='line', value_name='value')
    
    if type=='Altair Heatmap':
        data = np.random.rand(10, 10)
        data = pd.DataFrame(data, columns=[f"Column {i+1}" for i in range(10)])

        melted_data = data.reset_index().melt('index')
        melted_data.columns = ['y', 'x', 'value']
        
        return melted_data