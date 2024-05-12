import streamlit as st

# ------------------------------------------------------------------------------
# --------------------------------- Main settings ------------------------------
# ------------------------------------------------------------------------------
# Set page configuration options
st.set_page_config(
    layout="wide", 
    page_title="Humidity: Conclusion",
    page_icon="✍️",
)

# create columns
colA, colB, colC = st.columns([0.30,0.6,0.30])

with colB:

    # ---------------------------------
    # description
    st.markdown('# ✍️Conclusion')
    st.markdown('---')
    st.markdown('''At first glance, it can be stated that even if there is a chance of condensation, it is small, and if it does happen, there is enough ventilation so that this vapor does not get trapped. However, do not forget that the data are measured at 5 points. Local problems may still occur. Our conclusion only applies to the structure as a whole, that there is ventilation. A more accurate evaluation would be possible if the data were continuously measured and recorded automatically. I measured the data with everyday devices, so they also have uncertainty, but this error becomes negligible with a lot of data. There would still be plenty of opportunities to evaluate the data, but the important thing for me was to see that the structure cannot be damaged in the long term by any trapped vapor.''')

