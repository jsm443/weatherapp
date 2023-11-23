import pandas as pd
from math import cos, sin, radians
import numpy as np


# def add_wind_direction_arrows(fig, df, arrow_y_center=-5, arrow_length=35):
#     # Assuming 'Direction' is in degrees from 'North', adjust as necessary for your data

#     # Ensure 'datetime' column is in datetime format and set it as the DataFrame index
#     df["datetime"] = pd.to_datetime(df["datetime"])
#     df.set_index("datetime", inplace=True)

#     # Convert wind direction degrees to radians
#     df["rad"] = np.radians(df["Direction"])

#     # Calculate the arrow offset components based on wind direction
#     df["dx"] = arrow_length * np.sin(df["rad"])
#     df["dy"] = arrow_length * np.cos(df["rad"])

#     # Resample the data to get one point per hour
#     hourly_data = df.resample("H").first()

#     for i, row in hourly_data.iterrows():
#         fig.add_annotation(
#             x=i,  # X position (timestamp)
#             y=arrow_y_center,  # Y position (fixed at -5)
#             ax=row["dx"],  # X offset in pixels
#             ay=row["dy"],  # Y offset in pixels
#             xref="x",
#             yref="y",
#             axref="pixel",
#             # ayref="pixel",
#             showarrow=True,
#             arrowhead=2,
#             arrowsize=1,
#             arrowwidth=2,
#             arrowcolor="blue",
#         )


def add_wind_direction_arrows(fig, df, arrow_y_center=-5, arrow_length=35):
    # Ensure 'datetime' column is in datetime format and set it as the DataFrame index
    df.loc["datetime"] = pd.to_datetime(df["datetime"])
    df.set_index("datetime", inplace=True)

    # Resample the data to get one point per hour
    hourly_data = df.resample("H").first()

    for i, row in hourly_data.iterrows():
        if pd.notnull(row["Direction"]):
            # Convert wind direction to radians
            angle_rad = radians(row["Direction"])
            # Calculate the x and y components of the arrow
            dx = arrow_length * sin(angle_rad)
            dy = arrow_length * cos(angle_rad)

            # Add arrow annotation
            fig.add_annotation(
                x=i,  # X position (timestamp)
                y=arrow_y_center,  # Y position (fixed at arrow_y_center)
                ax=-dx,  # X offset in pixels (keep this as 0)
                ay=dy,  # if dy < 0 else -dy,  # Y offset in pixels (invert if necessary)
                xref="x",
                yref="y",
                axref="pixel",
                ayref="pixel",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="blue",
            )

    # Adjust the layout to accommodate the annotations
    fig.update_layout(
        xaxis=dict(
            domain=[0.05, 0.95],  # Adjust as needed to make space for annotations
            zeroline=True,  # Keep the zero line
            zerolinecolor="black",  # Color of the zero line
            zerolinewidth=2,  # Width of the zero line
            showticklabels=True,  # Show x-axis tick labels
        ),
        yaxis=dict(
            range=[
                -10,
                df["Gust"].max() + 10,
            ],  # Adjust y-axis to fit arrows
        ),
        # Other layout parameters...
    )
