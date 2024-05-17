import streamlit as st
import pandas as pd

# Add a lighter blue background to the page and chart, center the title and center the content of the page
st.markdown(
    """
    <style>
    .stApp {
        background-color: #E0FFFF;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    h1 {
        text-align: center;
        color: #000000;
    }
    .css-1aumxhk {
        background-color: #E0FFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use st.markdown with HTML to center the title
st.markdown("<h1>Uber pickups in NYC</h1>", unsafe_allow_html=True)

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

# Create a new column with the day of the week
data['day_of_week'] = data[DATE_COLUMN].dt.strftime('%A')

# Dropdown to select days
days_to_select = st.selectbox('Select day', sorted(data[DATE_COLUMN].dt.strftime('%A, %d-%m-%Y').unique()))
selected_data = data[data[DATE_COLUMN].dt.strftime('%A, %d-%m-%Y') == days_to_select]

st.subheader(f'Number of pickups by hour for selected day: {days_to_select}')
hist_values = selected_data[DATE_COLUMN].dt.hour.value_counts().sort_index()
st.bar_chart(hist_values)

st.subheader(f'Map of pickups for selected day: {days_to_select}')
st.map(selected_data)
