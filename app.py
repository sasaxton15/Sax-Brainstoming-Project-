import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px

@st.cache(ttl=60*5,max_entries=20) 
def load_data():
    data = pd.read_json('https://covidtracking.com/api/states')   
    return data

data = load_data() 


 
st.markdown('<style>description{color: blue;}</style>', unsafe_allow_html=True) 
st.title('🦠Covid-19 Impact in the US') 
st.markdown("<description>The objectve of this website is to offer an on-going assessment of COVID-19's impact in the US." + " This website gives you the real-time impact analysis of confirmed," + "active, recovered, and death cases of Covid-19 on National-, State-, and District-level basis." + "The website's data is updated every 5 minutes in order to ensure the delivery of true and" + "accurate data. </description>", unsafe_allow_html= True) 
st.sidebar.title('Select the parameters to analyze Covid-19 situation')  


st.sidebar.checkbox("Show Analysis by State", True, key=1)
select = st.sidebar.selectbox('Select a State',data['state'])
#get the state selected in the selectbox
state_data = data[data['state'] == select]
select_status = st.sidebar.radio("Covid-19 patient's status", ('positive',
'recovered', 'death', 'negative'))  

def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Status':['positive', 'recovered', 'death', 'negative'],
    'Number of cases':(dataset.iloc[0]['positive'],
    dataset.iloc[0]['recovered'], dataset.iloc[0]['death'], dataset.iloc[0]['negative'])})
    return total_dataframe 

State_total = get_total_dataframe(state_data)
if st.sidebar.checkbox("Show Analysis by State", True, key=2):
    st.markdown("## **State level analysis**")
    st.markdown("### Overall Confirmed, Recovered and " +
    "Deaths cases in %s yet" % (select))
    if not st.checkbox('Hide Graph', False, key=1):
        State_total_graph = px.bar(
        State_total, 
        x='Status',
        y='Number of cases',
        labels={'Number of cases':'Number of cases in %s' % (select)},
        color='Status')
        st.plotly_chart(State_total_graph)

def get_table():
    datatable = data[['state', 'positive', 'recovered', 'negative','death']].sort_values(by=['positive'], ascending=False)
    datatable = datatable[datatable['state'] != 'state unassigned']
    return datatable
datatable = get_table()
st.markdown("### Covid-19 cases in the US")
st.markdown("The following table gives you a real-time analysis of the confirmed, active, recovered and deceased cases of Covid-19 pertaining to each state in the US.")
st.dataframe(datatable) # will display the dataframe
st.table(datatable)# will display the table