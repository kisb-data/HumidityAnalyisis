import pandas as pd
import os
import ast

# ------------------------------------------------------------------------------
# convert absolute relative humidity to absolute
def relative_humidity_to_absolute(temp_celsius, relative_humidity):

    # Convert temperature to Kelvin
    temp_kelvin = temp_celsius + 273.15
    
    # Calculate saturation vapor pressure
    saturation_vapor_pressure = 6.112 * 10**(7.5 * temp_celsius / (temp_celsius + 237.7))
    
    # Calculate actual vapor pressure
    actual_vapor_pressure = saturation_vapor_pressure * relative_humidity / 100.0
    
    # Calculate absolute humidity
    absolute_humidity = 0.622 * actual_vapor_pressure / temp_kelvin * 1000.0  # Multiply by 1000 to convert to g/m^3

    return absolute_humidity


# ------------------------------------------------------------------------------
# create absulute humidity data, if is cashed, changes will not be don after refresh site
#@st.cache_resource
def GetData():

    # import humidity data
    df = pd.read_excel(os.path.dirname(os.path.abspath(__file__))+'\\Humidity data\\Humidity.xls')

    # take only relevant columns(need delete another)
    df = df.iloc[:, :14].copy()

    # remove nans and zeros
    df.dropna(inplace=True)

    # convert date and time to 1 datetime column and set it as index
    df['datetime'] = pd.to_datetime(df['Dátum'].astype(str) + ' ' + df['Idő'].astype(str))
    df.set_index('datetime', inplace=True)
    df.drop(['Dátum', 'Idő'], axis=1, inplace=True)

    # create absolute humidity dataframe
    abs_hum = pd.DataFrame()
    for i in range(0, len(df.columns)-1, 2):
        temp_celsius = df.iloc[:, i]
        relative_humidity = df.iloc[:, i]
        abs_hum[df.columns[i][0:len(df.columns[i])-2]] = relative_humidity_to_absolute(temp_celsius, relative_humidity)

    # absolute humidity dataframe
    rel_hum = pd.DataFrame()
    for i in range(1, len(df.columns), 2):
        rel_hum[df.columns[i]] = df[df.columns[i]]
    
    # temperature dataframe
    temp = pd.DataFrame()
    for i in range(0, len(df.columns), 2):
        temp[df.columns[i]] = df[df.columns[i]]

    return abs_hum, rel_hum, temp

# ------------------------------------------------------------------------------
# import chart data, if is cashed, changes will not be don after refresh site
#@st.cache_resource 
def GetChartData():
    path = os.path.dirname(os.path.abspath(__file__))+"\\.streamlit\\Humidity_chart.csv"
    ChartPropDF = pd.DataFrame()
    if os.path.exists(path):
        ChartPropDF = pd.read_csv(path, delimiter=';')
        ChartPropDF ['ChartValueColors'] = ChartPropDF ['ChartValueColors'].apply(ast.literal_eval)

    return ChartPropDF
