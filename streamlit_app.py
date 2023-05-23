import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load data
@st.cache
def load_data():
    data = pd.read_csv('your_data.csv')
    return data

df = load_data()

# Initialize the network
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

# add nodes for 'person'
persons = df['RecordID'].unique()
for person in persons:
    person_str = str(person)
    net.add_node(person_str, label=person_str, color='green')

# add nodes for other categories and connect them with 'person'
categories = df.columns.to_list()
categories.remove('RecordID')

for category in categories:
    unique_values = df[category].unique()
    for value in unique_values:
        value_str = str(value)
        net.add_node(f'{category}_{value_str}', label=value_str, color='red')
        subset = df[df[category] == value]
        for i in subset['RecordID']:
            net.add_edge(str(i), f'{category}_{value_str}')
            
# display the graph
net.show('example.html')
st.components.v1.html(net.HTML, height=600)
