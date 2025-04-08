import plotly.express as px
import pandas as pd
import streamlit as st

from streamlit_timeline import timeline


class PlotGenerator:

    def __init__(self):
        return

    def plot_gdelt_pie_chart(self, df: pd.DataFrame, column_name: str) -> px.pie:
        """
        Generates a pie chart from a DataFrame based on the specified column.

        This version handles rows containing comma-separated values and counts occurrences of each item.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column for which the pie chart should be generated.
        """
        # Split the values in the column by commas, strip any extra whitespace, and flatten the list
        split_values = df[column_name].str.split(",").explode().str.strip()

        # Count the occurrences of each unique value
        column_counts = split_values.value_counts().reset_index(name="counts")
        column_counts.columns = [column_name, "counts"]
        title = column_name.replace("_", " ")
        # Create the pie chart using Plotly
        fig = px.pie(
            column_counts,
            names=column_name,
            color_discrete_sequence=px.colors.qualitative.Set3,
            values="counts",
            title=f"{title} Distribution",
            hole=0.3,
            labels={column_name: column_name, "counts": "Count"},
            color=column_name,
        )
        return fig

    def plot_pie_chart(self, df: pd.DataFrame, column_name: str) -> px.pie:
        """
        Generates a pie chart from a DataFrame based on the specified column.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column for which the pie chart should be generated.
        """
        # Group the data by the specified column and count occurrences
        column_counts = df.groupby(column_name).size().reset_index(name="counts")
        title = column_name.replace("_", " ").capitalize()
        # Create the pie chart using Plotly
        fig = px.pie(
            column_counts,
            names=column_name,
            color_discrete_sequence=px.colors.qualitative.Set3,
            values="counts",
            title=f"{title} Distribution",
            hole=0.3,
            labels={column_name: column_name, "counts": "Count"},
            color=column_name,
        )
        return fig

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
            title=f"{freq.capitalize()} Activity",
            labels={
                "period": f"Period ({freq.capitalize()})",
                "row_count": "Activity",
            },
        )
        return fig

    def _plot_acled_timeline_(self, df: pd.DataFrame, datetime_column: str):
        """
        Generates and display a timeline plot with event types and notes.

        Parameters:
        df (pd.DataFrame): The input DataFrame.
        datetime_column (str): The name of the datetime column in the DataFrame.
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
        timeline(final_timeline, height=600)

    def _plot_gdelt_timeline_(self, df: pd.DataFrame, datetime_column: str):
        """
        Generates a timeline plot with event types and notes, handling duplicated headlines by combining URLs.

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

            # Group by "Headline" and aggregate links into a list
            grouped = (
                subset.groupby("Headline")
                .agg(
                    links=("link", lambda x: list(x))  # Aggregate the links into a list
                )
                .reset_index()
            )

            date_notes = []

            # Iterate through the grouped headlines and links
            for idx, row in grouped.iterrows():
                headline = row["Headline"]
                links = row["links"]

                # Create the note with a combined list of URLs for each headline
                links_html = "<br>".join(
                    [f"<a href='{link}' target='_blank'>{link}</a>" for link in links]
                )
                note = f"<b>{headline}</b><br>{links_html}"

                # Append the note to date_notes (avoiding duplicates)
                if note not in date_notes:
                    date_notes.append(note)

            # Create a dictionary for the event
            event_dict = {
                "media": {
                    "url": "",  # You can replace with appropriate media URL
                    "credit": "",  # Optionally add credits
                },
                "start_date": {
                    "year": date.year,
                    "month": date.month,
                    "day": date.day,
                },
                "text": {
                    "headline": f"News on {date}",
                    "text": "<br>".join(
                        date_notes
                    ),  # Join notes with <br> for line breaks
                },
            }

            # Add the event to the final timeline
            final_timeline["events"].append(event_dict)

        # Call the timeline function to render the timeline
        timeline(final_timeline, height=600)
