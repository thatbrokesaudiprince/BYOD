import plotly.express as px
import pandas as pd
import streamlit as st

from streamlit_timeline import timeline


class PlotGenerator:

    def __init__(self):
        return

    def plot_pie_chart(self, df: pd.DataFrame, column_name: str) -> px.pie:
        """
        Generates a pie chart from a DataFrame based on the specified column.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column for which the pie chart should be generated.
        """
        # Group the data by the specified column and count occurrences
        column_counts = df.groupby(column_name).size().reset_index(name="counts")

        # Create the pie chart using Plotly
        fig = px.pie(
            column_counts,
            names=column_name,
            color_discrete_sequence=px.colors.qualitative.Set3,
            values="counts",
            title=f"{column_name} Distribution",
            hole=0.3,
            labels={column_name: column_name, "counts": "Count"},
            color=column_name,
        )
        return fig

        # st.plotly_chart(fig=fig)

    def plot_time_series(self, df, datetime_column, freq="monthly") -> px.line:
        """
        Plots a graph showing the row count by selected time frequency (daily, monthly, or yearly).

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        datetime_column (str): The name of the datetime column in the DataFrame.
        freq (str): The frequency for grouping the data. Options are:
                    'daily', 'monthly', 'yearly'.

        Returns:
        None: Displays the plot.
        """
        # Ensure the datetime column is in datetime format
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors="coerce")

        # Group the data by the selected frequency (daily, monthly, or yearly)
        if freq == "daily":
            df["period"] = df[datetime_column].dt.date
        elif freq == "monthly":
            df["period"] = df[datetime_column].dt.to_period("M")  # Monthly period
        elif freq == "yearly":
            df["period"] = df[datetime_column].dt.to_period("Y")  # Yearly period
        else:
            raise ValueError("Frequency must be 'daily', 'monthly', or 'yearly'.")

        # Convert Period objects to string for compatibility with Plotly
        df["period"] = df["period"].astype(str)

        # Group by the new period and count the number of rows in each period
        count_by_period = df.groupby("period").size().reset_index(name="row_count")

        # Plot the result using Plotly
        fig = px.line(
            count_by_period,
            x="period",
            y="row_count",
            title=f"Mentions by {freq.capitalize()}",
            labels={
                "period": f"Period ({freq.capitalize()})",
                "row_count": "Mentions",
            },
        )
        return fig

    def _plot_timeline_(self, df: pd.DataFrame, datetime_column: str) -> dict:
        """
        Generates a timeline plot with event types and notes.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        datetime_column (str): The name of the datetime column in the DataFrame.

        Returns:
        dict: A Plotly timeline object (can be displayed with plotly.express).
        """
        # Ensure the datetime column is in datetime format
        df[datetime_column] = pd.to_datetime(df[datetime_column], errors="coerce")

        # Placeholder for the final structure
        final_timeline = {
            "title": {
                "text": {
                    "headline": "Event Timeline",
                }
            },
            "events": [],
        }

        # Iterate through unique event dates to prepare event data for the timeline
        for date in df[
            datetime_column
        ].dt.date.unique():  # Use .dt.date to work with only the date part
            # Filter the dataframe for the current date
            subset = df[df[datetime_column].dt.date == date]

            # Iterate through unique event types
            for event_type in subset["event_type"].unique():
                event_type_notes = (
                    []
                )  # List to store the notes for the current event type
                event_type_subset = subset[subset["event_type"] == event_type]

                # Iterate through the rows of the event type subset
                for idx, row in event_type_subset.iterrows():
                    # Append the note if it's not already in the list
                    if row["notes"] not in event_type_notes:
                        event_type_notes.append(row["notes"])

                # Create a dictionary for the event
                event_dict = {
                    "media": {
                        "url": "",  # You can replace with appropriate media URL
                        "caption": f"{event_type} (<a target=\"_blank\" href=''>credits</a>)",
                        "credit": "",  # Optionally add credits
                    },
                    "start_date": {
                        "year": date.year,
                        "month": date.month,
                        "day": date.day,
                    },
                    "text": {
                        "headline": f"{event_type}<br>Event Notes",
                        "text": "<br>".join(
                            set(event_type_notes)
                        ),  # Join notes with <br> for line breaks
                    },
                }

                # Add the event to the final timeline
                final_timeline["events"].append(event_dict)

        # Call the timeline function to render the timeline
        timeline(final_timeline, height=800)

    def plot_notes_per_event_type_per_day(self, df: pd.DataFrame) -> px.bar:
        """
        Plots a bar chart showing the number of notes per event type per day.

        Parameters:
        df (pd.DataFrame): The input DataFrame.

        Returns:
        px.bar: A Plotly bar chart displaying the count of notes per event type per day.
        """
        # Ensure the datetime column is in datetime format
        df["event_date"] = pd.to_datetime(df["event_date"], errors="coerce")

        # Group by event_date and event_type, and count the number of notes per group
        note_counts = (
            df.groupby(["event_date", "event_type"])
            .size()
            .reset_index(name="note_count")
        )

        # Create a bar chart with Plotly
        fig = px.bar(
            note_counts,
            x="event_date",
            y="note_count",
            color="event_type",
            title="Number of Notes per Event Type per Day",
            labels={"event_date": "Event Date", "note_count": "Number of Notes"},
            barmode="stack",  # Stacked bar chart to show notes for each event type
        )
        return fig
        # Display the plot
        # st.plotly_chart(fig)
