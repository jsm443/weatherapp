from flask import Flask
from dash import html, dcc, Dash
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
import data_store
from wind_direction_annotations import add_wind_direction_arrows

# Sample data (replace with your actual data retrieval method)
data = data_store.get_data()

# Convert the data to a DataFrame and sort by 'Epoch'
df = pd.DataFrame(data)
df = df.sort_values(by="Epoch")
df["datetime"] = pd.to_datetime(df["Epoch"], unit="s")

# Create a Flask instance
server = Flask(__name__)

# Initialize Dash app with Flask server
app = Dash(__name__, server=server)

# App layout with styled radio buttons
app.layout = html.Div(
    [
        dcc.Graph(id="wind-graph"),
        html.Div(
            dcc.RadioItems(
                id="time-selector",
                options=[
                    {"label": "  8 Hours  ", "value": "8h"},
                    {"label": " 24 Hours  ", "value": "24h"},
                    {"label": "  5 Days   ", "value": "5d"},
                ],
                value="8h",  # default value
                className="custom-radio-items",
            ),
            className="radio-container",
        ),
    ],
    style={
        "color": "#646464",
    },
)


# Callback to update the graph
@app.callback(
    Output("wind-graph", "figure"),
    [Input("time-selector", "value")],
)
def update_graph(selected_time):
    max_time = df["datetime"].max()
    if selected_time == "8h":
        filtered_df = df[df["datetime"] >= max_time - timedelta(hours=8)]
    elif selected_time == "24h":
        filtered_df = df[df["datetime"] >= max_time - timedelta(hours=24)]
    else:  # '5d'
        filtered_df = df[df["datetime"] >= max_time - timedelta(days=5)]

    # Create the plotly graph
    fig = go.Figure()

    # Trace for Average Speed (Primary Y-Axis)
    fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["Avg_Speed"],
            mode="lines",
            name="Average Speed",
            line=dict(color="#B31B1B"),  # Carnelian red
        )
    )

    # Trace for Gust (Secondary Y-Axis)
    fig.add_trace(
        go.Scatter(
            x=filtered_df["datetime"],
            y=filtered_df["Gust"],
            mode="lines",
            name="Gust",
            # yaxis="y2",  # Set to use the secondary y-axis
            line=dict(color="#5D5D5D"),  # Gray color
        )
    )

    # Update layout
    fig.update_layout(
        xaxis_title="Time",
        yaxis=dict(
            title="Wind Speed (MPH)",
            titlefont=dict(color="#646464"),
            tickfont=dict(color="#646464"),
            showgrid=True,
            gridcolor="#646464",
        ),
        plot_bgcolor="white",  # Background color
        font=dict(color="#646464"),  # Font color in gray
        xaxis=dict(
            showgrid=True,  # Enable gridlines on x-axis
            gridcolor="#646464",  # Set gridline color to gray for x-axis
            showline=True,  # Show the x-axis line
            linecolor="black",  # Color of the x-axis line
            linewidth=2,  # Width of the x-axis line
            ticks="outside",  # Position of the ticks ('outside', 'inside', or '')
            tickfont=dict(
                family="Arial",  # Font family
                size=12,  # Size of ticks
                color="black",  # Color of tick labels
            ),
        ),
    )

    add_wind_direction_arrows(fig, filtered_df)

    fig.add_hline(y=0)

    return fig


# Additional Flask routes can be defined here, if necessary

# Run the Flask app instead of Dash app
if __name__ == "__main__":
    server.run(debug=True)
