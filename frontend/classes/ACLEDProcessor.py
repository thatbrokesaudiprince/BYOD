# ACLEDProcessor.py

import pandas as pd
import streamlit as st
import itertools
import numpy as np
import datetime


def safe_convert_to_datetime(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Converts a dataframe column containing dates in string format like '7-Feb-25'
    or '30-Sept-24' into datetime objects. Handles errors gracefully.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    column_name (str): The name of the column containing date strings.

    Returns:
    pd.DataFrame: A DataFrame with the specified column converted to datetime objects.
    """
    # Attempt to convert to datetime
    try:
        # First attempt using '%d-%b-%y' for typical format
        df[column_name] = pd.to_datetime(
            df[column_name], format="%d-%b-%y", errors="raise"
        )
    except ValueError:
        # Handle edge cases where month abbreviation might be longer, or the day format might be inconsistent
        df[column_name] = pd.to_datetime(df[column_name], errors="coerce")

    return df


class ACLEDProcessor:
    def __init__(self, ACLED_FILES):
        """Initilaizes the ACLEDProcessor class"""

        self.column_definition = {
            "event_id_cnty": "A unique alphanumeric event identifier by number and country acronym. This identifier remains constant even when the event details are updated.",
            "event_date": "The date on which the event took place. Recorded as Year-Month-Day.",
            "year": "The year in which the event took place.",
            "time_precision": "A numeric code between 1 and 3 indicating the level of precision of the date recorded for the event. The higher the number, the lower the precision.",
            "disorder_type": "The disorder category an event belongs to.",
            "event_type": "The type of event; further specifies the nature of the event.",
            "sub_event_type": "A subcategory of the event type.",
            "actor1": "One of two main actors involved in the event (does not necessarily indicate the aggressor).",
            "assoc_actor_1": "Actor(s) involved in the event alongside ‘Actor 1’ or actor designations that further identify ‘Actor 1’",
            "inter1": "A text value indicating the type of ‘Actor 1’ (for more, see the section Actor Names, Types, and ‘Inter’ Codes).",
            "actor2": "One of two main actors involved in the event (does not necessarily indicate the target or victim).",
            "assoc_actor_2": "Actor(s) involved in the event alongside ‘Actor 2’ or actor designation further identifying ‘Actor 2’.",
            "inter2": "A text value indicating the type of ‘Actor 2’",
            "interaction": "A text value based on a combination of ‘Inter 1’ and ‘Inter 2’ indicating the two actor types interacting in the event (for more, see the section Actor Names, Types, and ‘Inter’ Codes).",
            "civilian_targeting": "This column indicates whether the event involved civilian targeting. ",
            "iso": "A unique three-digit numeric code assigned to each country or territory according to ISO 3166.",
            "region": "The region of the world where the event took place.",
            "country": "The country or territory in which the event took place.",
            "admin1": "The largest sub-national administrative region in which the event took place.",
            "admin2": "The second largest sub-national administrative region in which the event took place",
            "admin3": "The third largest sub-national administrative region in which the event took place.",
            "location": "The name of the location at which the event took place",
            "latitude": "The latitude of the location in four decimal degrees notation (EPSG:4326)",
            "longitude": "The longitude of the location in four decimal degrees notation (EPSG:4326)",
            "geo_precision": "A numeric code between 1 and 3 indicating the level of certainty of the location recorded for the event. The higher the number, the lower the precision.",
            "source": "The sources used to record the event. Separated by a semicolon.",
            "source_scale": "An indication of the geographic closeness of the used sources to the event",
            "notes": "A short description of the event.",
            "fatalities": "The number of reported fatalities arising from an event. When there are conflicting reports, the most conservative estimate is recorded.",
            "tags": "Additional structured information about the event. Separated by a semicolon",
            "timestamp": "An automatically generated Unix timestamp that represents the exact date and time an event was uploaded to the ACLED API.",
        }

        self.data = self._store_data_(ACLED_FILES)

    def _store_data_(self, ACLED_FILES: list) -> pd.DataFrame:
        # Initialize empty dataframe to store all data
        all_acled_data = pd.DataFrame()
        # Iterated through mutliples files from streamlit file uploader
        for file in ACLED_FILES:
            try:
                # Read current file
                current_file_data = pd.read_csv(file)
                # Validate file
                if list(current_file_data) == list(self.column_definition.keys()):
                    # Concatenate data
                    all_acled_data = pd.concat([current_file_data, all_acled_data])
                else:
                    st.info(
                        f"Skipping {file} \nReason: does not conform to ACLED data format"
                    )
            except Exception as e:
                st.error(f"Error reading {file}: {e}")
        if not all_acled_data.empty:
            all_acled_data.sort_values(by="event_date", ascending=True, inplace=True)
        # return all data
        return safe_convert_to_datetime(all_acled_data, "event_date")

    def _get_columns_(self) -> list:
        """Returns a list of all column names"""
        return list(self.column_definition.keys())

    def _get_definition_(self, col: str):
        """Returns the definition of a column"""
        return self.column_definition[col]

    def _get_disorder_types_(self) -> list:
        """Returns a list of all event types available"""
        return list(self.data["disorder_type"].unique()) if not self.data.empty else []

    def _get_event_types_(self) -> list:
        """Returns a list of all event types available"""
        return list(self.data["event_type"].unique()) if not self.data.empty else []

    def _get_sub_event_types_(self) -> list:
        """Returns a list of all event types available"""
        return list(self.data["sub_event_type"].unique()) if not self.data.empty else []

    def _get_description_(self, event_id_cnty: str) -> str:
        """Returns the event description note for a unique event"""
        return (
            self.data["note"][self.data["event_id_cnty"] == event_id_cnty]
            if not self.data.empty
            else ""
        )

    def _get_actors_(self) -> list:
        """Returns a list of all associated actors"""
        cols = ["actor1", "assoc_actor_1", "actor2", "assoc_actor_2"]
        actors = []

        for col in cols:
            temp = (
                self.data[col].dropna().unique() if not self.data.empty else []
            )  # Remove NaN values and get unique actors
            actors.append(temp.tolist())

        result = (
            set(itertools.chain.from_iterable(actors)) if len(actors) > 0 else set()
        )  # Flatten the list and remove duplicates
        return list(
            result
        )  # Convert the set back to list if you need a list as a return type

    def _get_events_(
        self,
        actors: list = None,
        disorder_types: list = None,
        event_types: list = None,
        sub_event_types: list = None,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        """Return a subset of the original dataframe which matches all the filters"""

        if self.data.empty:
            return pd.DataFrame()

        # Create a boolean mask initialized to True for all rows
        mask = pd.Series(True, index=self.data.index)

        # Apply filters only if the corresponding list is provided
        if actors:
            mask &= (
                self.data["actor1"].isin(actors)
                | self.data["assoc_actor_1"].isin(actors)
                | self.data["actor2"].isin(actors)
                | self.data["assoc_actor_2"].isin(actors)
            )

        if event_types:
            mask &= self.data["event_type"].isin(event_types)

        if disorder_types:
            mask &= self.data["disorder_type"].isin(disorder_types)

        if sub_event_types:
            mask &= self.data["sub_event_type"].isin(sub_event_types)
        print(self.data[mask])

        if start_date:
            print("START", start_date)
            mask &= self.data["event_date"] >= start_date

        if end_date:
            print("END", end_date)
            mask &= self.data["event_date"] <= end_date
        print(self.data[mask])
        return self.data[mask]
