import pandas as pd
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    df1 = pd.read_csv('women_on_remand.csv')
    df2 = pd.read_csv('women_received_into_prison.csv')
    df3 = pd.read_csv('women_on_supervised_orders_current.csv')
    df4 = pd.read_csv('women_on_supervised_orders_starting.csv')
    return df1, df2, df3, df4

df1, df2, df3, df4 = load_data()

# Create network graph
def create_network_graph(df):
    G = nx.Graph()
    root_values = []
    for i in range(len(df)):
        root = df.columns[0] if 'id' not in df.columns else 'id' # Use the first column if 'id' does not exist
        root_value = df.iloc[i][root]
        root_values.append(root_value)
        G.add_node(root_value)
        for col in df.columns:
            if col != root:
                G.add_node(df.iloc[i][col])
                G.add_edge(root_value, df.iloc[i][col])
    return G, root_values

# Draw network graph
def draw_network_graph(G, root_values):
    fig, ax = plt.subplots(figsize=(8,6))
    node_colors = ["green" if node in root_values else "red" for node in G.nodes()]
    nx.draw(G, with_labels=True, node_color=node_colors, ax=ax)
    st.pyplot(fig)

# Display statistics
def display_statistics(df, root_column):
    for column in df.columns:
        if column != root_column:
            df_column_stats = df[column].value_counts().to_frame().reset_index()
            df_column_stats.columns = [column, 'Count']
            if not df_column_stats.empty and not df_column_stats[column].astype(str).str.contains('None').any():
                st.write(f"Statistics for {column}")
                st.dataframe(df_column_stats)

st.header('Victoria Corrections Data')
st.write('Green = Case')
st.write('Red = Characteristics')

# Create and draw network graph for each dataframe
st.header('Women on Remand')
G1, root_values1 = create_network_graph(df1)
draw_network_graph(G1, root_values1)
root_column1 = df1.columns[0] if 'id' not in df1.columns else 'id'
display_statistics(df1, root_column1)

st.header('Women Received into Prison')
G2, root_values2 = create_network_graph(df2)
draw_network_graph(G2, root_values2)
root_column2 = df2.columns[0] if 'id' not in df2.columns else 'id'
display_statistics(df1, root_column2)

st.header('Women on Supervised Orders (Current)')
G3, root_values3 = create_network_graph(df3)
draw_network_graph(G3, root_values3)
root_column3 = df3.columns[0] if 'id' not in df3.columns else 'id'
display_statistics(df3, root_column3)

st.header('Women on Supervised Orders (Starting)')
G4, root_values4 = create_network_graph(df4)
draw_network_graph(G4, root_values4)
root_column4 = df4.columns[0] if 'id' not in df4.columns else 'id'
display_statistics(df4, root_column4)
