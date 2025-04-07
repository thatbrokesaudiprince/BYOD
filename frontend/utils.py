# utils.py
import pandas as pd
import itertools
import streamlit as st
import plotly.express as px
from classes.MapGenerator import MapGenerator
from classes.ACLEDProcessor import ACLEDProcessor
from classes.PlotGenerator import PlotGenerator
from classes.CELLEXProcessor import CELLEXProcessor


def safe_convert_to_datetime(df, column_name):
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


def initialize_map(
    map_generator_class: MapGenerator,
    tiles: str = "https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
    attr: str = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://cartodb.com/attributions">CartoDB</a>',
):
    """Initializes the map only once."""
    return map_generator_class(tiles=tiles, attr=attr)


def get_global_actors() -> list:
    """Returns a list of all the actors available"""

    global_actors = []
    if "acled_processor" in st.session_state:
        global_actors.append(st.session_state.acled_processor._get_actors_())
    if "cellex_processor" in st.session_state:
        global_actors.append(st.session_state.cellex_processor._get_actors_())
    if "gdelt_processor" in st.session_state:
        global_actors.append(st.session_state.gdelt_processor._get_actors_())
    return list(set(itertools.chain.from_iterable(global_actors)))


def get_global_event_types() -> list:
    """Returns a list of all the event types available"""

    global_event_types = []
    if "acled_processor" in st.session_state:
        global_event_types.append(st.session_state.acled_processor._get_event_types_())
    # if "cellex_processor" in st.session_state:
    #     global_event_types.append(st.session_state.cellex_processor._get_event_types_())
    if "gdelt_processor" in st.session_state:
        global_event_types.append(st.session_state.gdelt_processor._get_event_types_())
    return list(set(itertools.chain.from_iterable(global_event_types)))


def get_global_sub_event_types() -> list:
    """Returns a list of all the sub event types available"""
    global_sub_event_types = []
    if "acled_processor" in st.session_state:
        global_sub_event_types.append(
            st.session_state.acled_processor._get_sub_event_types_()
        )
    # if "cellex_processor" in st.session_state:
    #     global_sub_event_types.append(
    #         st.session_state.cellex_processor._get_sub_event_types_()
    #     )
    if "gdelt_processor" in st.session_state:
        global_sub_event_types.append(
            st.session_state.gdelt_processor._get_sub_event_types_()
        )
    return list(set(itertools.chain.from_iterable(global_sub_event_types)))


def get_global_disorder_types() -> list:
    """Returns a list of all the disorder types available"""
    global_disorder_types = []
    if "acled_processor" in st.session_state:
        global_disorder_types.append(
            st.session_state.acled_processor._get_disorder_types_()
        )
    if "cellex_processor" in st.session_state:
        global_disorder_types.append(
            st.session_state.cellex_processor._get_disorder_types_()
        )
    if "gdelt_processor" in st.session_state:
        global_disorder_types.append(
            st.session_state.gdelt_processor._get_disorder_types_()
        )
    return list(set(itertools.chain.from_iterable(global_disorder_types)))


def initialize_variables() -> None:
    """Initialize session state variables if they have not been previously initialized"""
    if "plot_generator" not in st.session_state:

        st.session_state.plot_generator = PlotGenerator()

    # if "map_generator" not in st.session_state:
    st.session_state.map_generator = MapGenerator(
        tiles="https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://cartodb.com/attributions">CartoDB</a>',
    )
    if "plot_generator" not in st.session_state:
        st.session_state.plot_generator = PlotGenerator()

    if (
        "acled_data" in st.session_state
        or "gdelt_data" in st.session_state
        or "cellex_data" in st.session_state
    ):
        st.session_state.global_actors = get_global_actors()
        st.session_state.global_event_types = get_global_event_types()
        st.session_state.global_sub_event_types = get_global_sub_event_types()
        st.session_state.global_disorder_types = get_global_actors()


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
    actors: list, disorder_types: list, event_types: list, sub_event_types: list
) -> None:
    """Use the values stored in the selected categories session state to update the acled_data session state"""
    if "acled_processor" in st.session_state:
        st.session_state.acled_data = safe_convert_to_datetime(
            st.session_state.acled_processor._get_events_(
                actors=actors,
                disorder_types=disorder_types,
                event_types=event_types,
                sub_event_types=sub_event_types,
            ),
            "event_date",
        )


def generate_actor_columns(category_col, plot_col, time_col):
    """Generate the multiselect and select box widges for Actors using predefined st.columns()"""
    with category_col:
        dashboard_actors_multiselect = st.multiselect(
            label="Select Actor(s)",
            options=st.session_state.global_actors,
            key="dashboard_actors",
        )
    with plot_col:
        dashboard_actors_plots = st.multiselect(
            label="Select Available Plots",
            options=["Frequency Distribution"],
            key="dashboard_actors_plots",
        )
    with time_col:
        dashboard_actors_time = st.selectbox(
            label="Select Time",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            key="dashboard_actors_time",
        )
    return dashboard_actors_multiselect, dashboard_actors_plots, dashboard_actors_time


def generate_event_type_columns(
    category_col, attribute_plot_col, column_plot_col, time_col
):
    """Generate the multiselect and select box widges for Event Types using predefined st.columns()"""

    with category_col:
        dashboard_event_types_multiselect = st.multiselect(
            label="Select Event Type(s)",
            options=st.session_state.global_event_types,
            key="dashboard_event_types",
        )
    with attribute_plot_col:
        dashboard_event_types_plots = st.multiselect(
            label="Select Attribute Plots",
            options=["Frequency Distribution"],
            key="dashboard_event_types_plots",
        )
    with column_plot_col:
        dashboard_event_types_plots = st.multiselect(
            label="Select Column Plots",
            options=["Value Distribution"],
            key="dashboard_event_types_plots",
        )
    with time_col:
        dashboard_event_types_time = st.selectbox(
            label="Select Time",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            key="dashboard_event_types_time",
        )
    return (
        dashboard_event_types_multiselect,
        dashboard_event_types_plots,
        dashboard_event_types_time,
    )


def generate_sub_event_type_columns(category_col, plot_col, time_col):
    """Generate the multiselect and select box widges for Sub Event Types using predefined st.columns()"""

    with category_col:
        dashboard_sub_event_types_multiselect = st.multiselect(
            label="Select Sub Event Type(s)",
            options=st.session_state.global_sub_event_types,
            key="dashboard_sub_event_types",
        )
    with plot_col:
        dashboard_sub_event_type_plots = st.multiselect(
            label="Select Available Plots",
            options=["Frequency Distribution"],
            key="dashboard_sub_event_types_plots",
        )
    with time_col:
        dashboard_sub_event_type_time = st.selectbox(
            label="Select Time",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            key="dashboard_sub_event_types_time",
        )
    return (
        dashboard_sub_event_types_multiselect,
        dashboard_sub_event_type_plots,
        dashboard_sub_event_type_time,
    )


def generate_disorder_type_columns(category_col, plot_col, time_col):
    """Generate the multiselect and select box widges for Disorder Types using predefined st.columns()"""

    with category_col:
        dashboard_disorder_type_multiselect = st.multiselect(
            label="Select Disorder Type(s)",
            options=st.session_state.global_disorder_types,
            key="dashboard_disorder_type",
        )
    with plot_col:
        dashboard_disorder_type_plots = st.multiselect(
            label="Select Available Plots",
            options=["Frequency Distribution"],
            key="dashboard_disorder_type_plots",
        )
    with time_col:
        dashboard_disorder_type_time = st.selectbox(
            label="Select Time",
            options=["Daily", "Weekly", "Monthly", "Yearly"],
            key="dashboard_disorder_type_time",
        )
    return (
        dashboard_disorder_type_multiselect,
        dashboard_disorder_type_plots,
        dashboard_disorder_type_time,
    )
