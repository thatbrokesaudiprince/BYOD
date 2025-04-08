# utils.py
import pandas as pd
import itertools
import streamlit as st
import plotly.express as px
import datetime
from classes.MapGenerator import MapGenerator
from classes.ACLEDProcessor import ACLEDProcessor
from classes.PlotGenerator import PlotGenerator
from classes.CELLEXProcessor import CELLEXProcessor
from classes.GDELTProcessor import GDELTProcessor


def initialize_variables() -> None:
    """Initialize session state variables if they have not been previously initialized"""
    tiles = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png"
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'

    if "plot_generator" not in st.session_state:

        st.session_state.plot_generator = PlotGenerator()

    st.session_state.map_generator = MapGenerator(
        tiles=tiles,
        attr=attr,
    )


def initialize_cellex_variables() -> None:
    """Initialize the cellex processor class and assign the unique values to the session state variables"""

    if "cellex_processor" not in st.session_state:
        st.session_state.cellex_processor = CELLEXProcessor(
            st.session_state.CELLEX_FILES
        )
        st.session_state.cellex_actors = (
            st.session_state.cellex_processor._get_actors_()
        )


def update_cellex_data(actors: list) -> None:
    """Use the values stored in the selected cellex filter session state to update the cellex_data session state variable"""

    if "cellex_processor" in st.session_state:
        st.session_state.cellex_data = (
            st.session_state.cellex_processor._get_meta_data_(cellexs=actors)
        )


def initialize_gdelt_variables() -> None:
    """Initialize the gdelt processor class and assign the unique values to the session state variables"""
    if "gdelt_processor" not in st.session_state:
        st.session_state.gdelt_processor = GDELTProcessor(st.session_state.GDELT_FILES)
        st.session_state.gdelt_countries_states = (
            st.session_state.gdelt_processor._get_countries_states_()
        )
        st.session_state.gdelt_organizations = (
            st.session_state.gdelt_processor._get_organizations_()
        )
        st.session_state.gdelt_sources = (
            st.session_state.gdelt_processor._get_sources_()
        )
        st.session_state.gdelt_persons = (
            st.session_state.gdelt_processor._get_persons_()
        )
        st.session_state.gdelt_other_mentions = (
            st.session_state.gdelt_processor._get_other_mentions_()
        )


def update_gdelt_data(
    persons: list,
    countries_states: list,
    sources: list,
    organizations: list,
    other_mentions: list,
    start_date: datetime,
    end_date: datetime,
) -> None:
    """Use the values stored in the selected gdelt session state to update the gdelt_data session state"""
    if "gdelt_processor" in st.session_state:
        st.session_state.gdelt_data = st.session_state.gdelt_processor._get_events_(
            persons=persons,
            sources=sources,
            organizations=organizations,
            countries_states=countries_states,
            other_mentions=other_mentions,
            start_date=start_date,
            end_date=end_date,
        )


def initialize_acled_variables() -> None:
    """Initialize the acled processor class and assign the unique values to the session state variables"""
    if "acled_processor" not in st.session_state:
        st.session_state.acled_processor = ACLEDProcessor(st.session_state.ACLED_FILES)
        st.session_state.acled_actors = st.session_state.acled_processor._get_actors_()
        st.session_state.acled_event_types = (
            st.session_state.acled_processor._get_event_types_()
        )
        st.session_state.acled_sub_event_types = (
            st.session_state.acled_processor._get_sub_event_types_()
        )
        st.session_state.acled_disorder_types = (
            st.session_state.acled_processor._get_disorder_types_()
        )


def update_acled_data(
    actors: list,
    disorder_types: list,
    event_types: list,
    sub_event_types: list,
    start_date: datetime,
    end_date: datetime,
) -> None:
    """Use the values stored in the selected categories session state to update the acled_data session state"""
    if "acled_processor" in st.session_state:
        st.session_state.acled_data = st.session_state.acled_processor._get_events_(
            actors=actors,
            disorder_types=disorder_types,
            event_types=event_types,
            sub_event_types=sub_event_types,
            start_date=start_date,
            end_date=end_date,
        )
