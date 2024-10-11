import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.title("Bristol Rovers Data Dashboard")
st.subheader("Compare players from the same or different datasets")

# Load the datasets
df1 = pd.read_csv("EFL L1 Overall Rank - Raw.csv")
df2 = pd.read_csv("dataset2.csv")  # Replace with your actual file path for dataset2.csv

# Add a column to each dataset to track their source
df1['dataset'] = 'EFL L1 Dataset'
df2['dataset'] = 'Performance Metrics Dataset'

# Uniform column for player names
df1['player'] = df1['player_name']  
df2['player'] = df2['Player']       

# Combine the datasets for player selection
combined_df = pd.concat([df1[['player', 'dataset']], df2[['player', 'dataset']]])

# Create two player selection dropdowns (can select from either dataset)
player1 = st.selectbox("Select Player 1", combined_df['player'].unique())
player2 = st.selectbox("Select Player 2", combined_df['player'].unique())

# Determine the dataset for each selected player
player1_dataset = combined_df[combined_df['player'] == player1]['dataset'].values[0]
player2_dataset = combined_df[combined_df['player'] == player2]['dataset'].values[0]

# Fetch player data from the respective dataset
if player1_dataset == 'EFL L1 Dataset':
    player1_data = df1[df1['player'] == player1]
else:
    player1_data = df2[df2['player'] == player1]

if player2_dataset == 'EFL L1 Dataset':
    player2_data = df1[df1['player'] == player2]
else:
    player2_data = df2[df2['player'] == player2]

# Display player data from both datasets
st.write(f"Data for {player1}:")
st.write(player1_data)

st.write(f"Data for {player2}:")
st.write(player2_data)

# Define metrics for radar chart and bar chart comparison (adjust as necessary)
player1_metrics = [
    player1_data['player_season_goals_90'].values[0] if player1_dataset == 'EFL L1 Dataset' else player1_data['Goals per 90'].values[0],
    player1_data['player_season_xa_90'].values[0] if player1_dataset == 'EFL L1 Dataset' else player1_data['xA per 90'].values[0],
    player1_data['player_season_shot_on_target_ratio'].values[0] if player1_dataset == 'EFL L1 Dataset' else player1_data['Shots on target, %'].values[0],
    player1_data['player_season_conversion_ratio'].values[0] if player1_dataset == 'EFL L1 Dataset' else player1_data['Goal conversion, %'].values[0]
]

player2_metrics = [
    player2_data['player_season_goals_90'].values[0] if player2_dataset == 'EFL L1 Dataset' else player2_data['Goals per 90'].values[0],
    player2_data['player_season_xa_90'].values[0] if player2_dataset == 'EFL L1 Dataset' else player2_data['xA per 90'].values[0],
    player2_data['player_season_shot_on_target_ratio'].values[0] if player2_dataset == 'EFL L1 Dataset' else player2_data['Shots on target, %'].values[0],
    player2_data['player_season_conversion_ratio'].values[0] if player2_dataset == 'EFL L1 Dataset' else player2_data['Goal conversion, %'].values[0]
]

metrics_labels = ['Goals/90', 'xA/90', 'Shots on Target Ratio', 'Conversion Ratio']

# Radar chart visualization
fig_radar = go.Figure()

fig_radar.add_trace(go.Scatterpolar(
    r=player1_metrics,
    theta=metrics_labels,
    fill='toself',
    name=player1
))

fig_radar.add_trace(go.Scatterpolar(
    r=player2_metrics,
    theta=metrics_labels,
    fill='toself',
    name=player2
))

fig_radar.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(max(player1_metrics), max(player2_metrics))])),
    showlegend=True
)

# Display the radar chart
st.plotly_chart(fig_radar)

# Bar chart visualization for comparison
bar_data = pd.DataFrame({
    'Metric': metrics_labels,
    'Player 1': player1_metrics,
    'Player 2': player2_metrics
})

# Reshaping the dataframe for group bar plotting
bar_data_melted = bar_data.melt(id_vars='Metric', var_name='Player', value_name='Value')

# Create the grouped bar chart
fig_bar = px.bar(bar_data_melted, x='Metric', y='Value', color='Player', barmode='group',
                 labels={'Value': 'Metric Value'}, title='Player Comparison Bar Chart')

# Display the bar chart
st.plotly_chart(fig_bar)

# Pizza Chart for Both Players
pizza_labels = metrics_labels
pizza_values_player1 = player1_metrics
pizza_values_player2 = player2_metrics

# Pizza chart visualization for Player 1
fig_pizza1 = go.Figure(go.Barpolar(
    r=pizza_values_player1,
    theta=pizza_labels,
    marker=dict(color=["#ff6347", "#4682b4", "#3cb371", "#ffa500"]),
    name=player1
))

fig_pizza1.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False,
    title=f'Pizza Chart for {player1}'
)

# Pizza chart visualization for Player 2
fig_pizza2 = go.Figure(go.Barpolar(
    r=pizza_values_player2,
    theta=pizza_labels,
    marker=dict(color=["#ff6347", "#4682b4", "#3cb371", "#ffa500"]),
    name=player2
))

fig_pizza2.update_layout(
    polar=dict(radialaxis=dict(visible=True)),
    showlegend=False,
    title=f'Pizza Chart for {player2}'
)

# Display the pizza charts
st.plotly_chart(fig_pizza1)
st.plotly_chart(fig_pizza2)