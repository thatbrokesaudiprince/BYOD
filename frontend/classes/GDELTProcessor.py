# GDELTProcessor.py

import pandas as pd
import streamlit as st
import itertools
import numpy as np


class GDELTProcessor:
    def __init__(self, GDELT_FILES):
        """Initilaizes the GDELTProcessor class"""

        self.column_mapper = {
            "V2ExtrasXML.Title": "Headline",
            "V2ExtrasXML.Author": "Source",
            "V2Persons.V1Person": "Mentioned Persons",
            "V2Orgs.V1Org": "Mentioned Organizations",
            "V2Locations.FullName": "Mentioned Countries/States",
            "V2Locations.LocationLatitude": "latitudes",
            "V2Locations.LocationLongitude": "longitudes",
            "location": "location",
            "V2ExtrasXML.PubTimestamp": "event_date",
            "V2DocId": "link",
            "V2EnhancedThemes.V2Theme": "Categories",
            "V21AllNames.Name": "Other Mentions",
        }

        self.data = self._store_data_(GDELT_FILES)
        self._format_time_()

    def _store_data_(self, GDELT_FILES: list) -> pd.DataFrame:
        # Initialize empty dataframe to store all data
        all_GDELT_data = pd.DataFrame()
        # Iterated through mutliples files from streamlit file uploader
        for file in GDELT_FILES:
            try:
                # Read current file
                current_file_data = pd.read_csv(file)

                # Concatenate data
                all_GDELT_data = pd.concat([current_file_data, all_GDELT_data])

            except Exception as e:
                st.error(f"Error reading {file}: {e}")
        # print(all_GDELT_data.head())
        # print("END OF STORE DATA FUNCTION")
        return all_GDELT_data[list(self.column_mapper.keys())]

    def _format_time_(self) -> None:
        self.data = self.data.rename(columns=self.column_mapper)
        self.data["event_date"] = pd.to_datetime(
            self.data["event_date"], format="%b %d, %Y @ %H:%M:%S.%f"
        )

    def _get_columns_(self) -> list:
        """Returns a list of all column names"""
        return list(self.column_mapper.values())

    def _get_other_mentions_(self) -> list:
        """Returns a list of all countries available"""
        unique_other_mentions = []
        for om in self.data["Other Mentions"].values:
            if om != "-":
                for a in om.split(","):
                    if a.strip() not in unique_other_mentions:
                        unique_other_mentions.append(a.strip())
        return unique_other_mentions if not self.data.empty else []

    def _get_countries_states_(self) -> list:
        """Returns a list of all countries available"""
        unique_countries = []
        for country in self.data["Mentioned Countries/States"].values:
            if country != "-":
                for a in country.split(","):
                    if a.strip() not in unique_countries:
                        unique_countries.append(a.strip())
        return unique_countries if not self.data.empty else []

    def _get_organizations_(self) -> list:
        """Returns a list of all organizations available"""
        unique_orgs = []
        for org in self.data["Mentioned Organizations"].values:
            if org != "-":
                for a in org.split(","):
                    if a.strip() not in unique_orgs:
                        unique_orgs.append(a.strip())
        return unique_orgs if not self.data.empty else []

    def _get_persons_(self) -> list:
        """Returns a list of all persons available"""
        unique_persons = []
        for person in self.data["Mentioned Persons"].values:
            if person != "-":
                for a in person.split(","):
                    if a.strip() not in unique_persons:
                        unique_persons.append(a.strip())
        return unique_persons if not self.data.empty else []

    def _get_sources_(self) -> list:
        """Returns a list of all sources available"""
        unique_authors = []
        for author in self.data["Source"].values:
            if author not in unique_authors:
                unique_authors.append(author)
        return unique_authors if not self.data.empty else []

    def _get_events_(
        self,
        persons: list = None,
        sources: list = None,
        organizations: list = None,
        countries_states: list = None,
        other_mentions: list = None,
        start_date=None,
        end_date=None,
    ) -> pd.DataFrame:
        """Return a subset of the original dataframe which matches all the filters"""

        if self.data.empty:
            return pd.DataFrame()

        # Default to class instance methods if no lists are provided
        start_date = start_date or self.data["event_date"].min()
        end_date = end_date or self.data["event_date"].max()
        persons = persons or self._get_persons_()
        sources = sources or self._get_sources_()
        organizations = organizations or self._get_organizations_()
        countries_states = countries_states or self._get_countries_states_()
        other_mentions = other_mentions or self._get_other_mentions_()

        # Ensure the start_date and end_date are datetime objects
        # start_date = pd.to_datetime(start_date)
        # end_date = pd.to_datetime(end_date)

        # Create a mask for all conditions
        mask = pd.Series(True, index=self.data.index)

        # Helper function to check if any filter term exists in the comma-separated string
        def contains_any(value, filter_list):
            if isinstance(value, str) and filter_list:
                value_list = [v.strip() for v in value.split(",")]
                return any(
                    term.lower() in [v.lower() for v in value_list]
                    for term in filter_list
                )
            return False

        # Apply filters for each category (persons, sources, organizations, countries_states, other_mentions)
        if persons:
            mask &= self.data["Mentioned Persons"].apply(
                lambda x: contains_any(x, persons)
            )

        if sources:
            mask &= self.data["Source"].apply(lambda x: contains_any(x, sources))

        if organizations:
            mask &= self.data["Mentioned Organizations"].apply(
                lambda x: contains_any(x, organizations)
            )

        if countries_states:
            mask &= self.data["Mentioned Countries/States"].apply(
                lambda x: contains_any(x, countries_states)
            )

        if other_mentions:
            mask &= self.data["Other Mentions"].apply(
                lambda x: contains_any(x, other_mentions)
            )

        # Apply date range filter
        mask &= (self.data["event_date"] >= start_date) & (
            self.data["event_date"] <= end_date
        )

        # Return the filtered data
        return self.data[mask]
