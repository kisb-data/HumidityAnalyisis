import toml
import pandas as pd
import os

# defaulr streamlit theme
def GetDefault():
    theme = pd.Series()
    theme['primaryColor'] = '#BCC3C4'
    theme['backgroundColor'] = '#414141'
    theme['secondaryBackgroundColor'] = '#60B4DE'
    theme['textColor'] = '#FFFFFF'
    theme['font'] = 'sans serif'

    return theme

# export config data
def data_to_toml(path, data, dict_name):

    # Convert Pandas Series to dictionary
    data = {dict_name: data.to_dict()}

    # remove previous version
    if os.path.exists(path):
        os.remove(path)

    # export
    with open(path, 'w') as f:
        toml.dump(data, f)

# import toml data
def data_from_toml(path, data):

    # import
    with open(path, 'r') as f:
        config_data = toml.load(f)

    # extract data
    data = config_data.get(data, {})

    # convert to series
    series = pd.Series(data)

    return series