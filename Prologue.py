import streamlit as st

# ------------------------------------------------------------------------------
# --------------------------------- Main settings ------------------------------
# ------------------------------------------------------------------------------
# Set page configuration options
st.set_page_config(
    layout="wide", 
    page_title="Humidity: Introduction",
    page_icon="✏️"
)

# ------------------------------------------------------------------------------
# ---------------------------------- Start page --------------------------------
# ------------------------------------------------------------------------------

# create columns
colA, colB, colC = st.columns([0.30,0.6,0.30])

with colB:

    # description
    st.markdown('# 📈 Humidity analysis')
    st.markdown('---')
    st.markdown('### Chapters:')
    st.markdown(' - ✏️Prologue:  Description of the project')
    st.markdown(' - 📈ExploreData:  About the dataset')
    st.markdown(' - 📆MonthlyStatement:  Better view in monthly resolution.')
    st.markdown(' - 👉CheckTheDewPoint:  See how close are we to possible condensation.')
    st.markdown(' - ✍️Conclusion:  Thinking about the result.')
    st.markdown('')
    st.markdown('')
    st.markdown('### Prologue: ')
    st.markdown('''I created this project in order to analise possibility of condensations in wooden structure of a house. To understand it all, we need to clarify a few things. Humidity is nothing but the presence of vaporised water in the air. Two metrics are used to describe this type of quantity, relative humidity and the absolute humidity. But what are these and how do these two relate to each other?  The relative humidity tells us what percentage of the maximum possible moisture is currently present in the air. The absolute humidity tells us how many gramms of moisture are contained in 1 cubic meter of air. If there is more moisture in the air than it can bind, the excess will condense on colder surfaces (this is the condensation which can cause the problem in case of a thermal bridge, or lack of ventillation in a variable temperature environment).  Air with a higher temperature can hold more vapor than a colder one with lower temperature, so it is important that the vapor can flow from the air, what ensures this is the vapor pressure. In order for the vapor pressure to be created, ventilation or vapor diffusion of the materials is necessary.''')

