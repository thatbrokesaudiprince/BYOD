import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
from utils import *

# Import utility functions

# Set page layout
st.set_page_config(layout="wide")

# Initialize session state variables if they don't exist
initialize_variables()

# Set data upload for sources
st.header("Data Files upload")

cellex_upload, acled_upload, gdelt_upload = st.columns(3)
with cellex_upload:
    st.session_state.CELLEX_FILES = st.file_uploader(
        label="Upload CELLEX data here!", accept_multiple_files=True
    )

with acled_upload:
    st.session_state.ACLED_FILES = st.file_uploader(
        label="Upload ACLED data here!", accept_multiple_files=True, type=[".csv"]
    )

with gdelt_upload:
    st.session_state.GDELT_FILES = st.file_uploader(
        label="Upload GDELT data here!", accept_multiple_files=True
    )

# Process ACLED Data
if len(st.session_state.ACLED_FILES) > 0:
    initialize_acled_variables()

    acled_filter_expander = st.expander("Select ACLED Filters Here")

    with acled_filter_expander:
        checkbox_col, multi_select_col = st.columns([0.2, 0.8])

        with checkbox_col:
            actors_checkbox = st.checkbox(
                f"Select all Acled Actors",
                value=True,
            )
            event_types_checkbox = st.checkbox(f"Select all Event Types", value=True)
            sub_event_types_checkbox = st.checkbox(f"Select all Sub Events", value=True)
            disorder_types_checkbox = st.checkbox(
                f"Select all Disorder Types", value=True
            )

        with multi_select_col:
            st.session_state.selected_actors = st.multiselect(
                label="Select Actor(s)", options=sorted(st.session_state.acled_actors)
            )
            st.session_state.selected_event_types = st.multiselect(
                label="Select Event(s)",
                options=sorted(st.session_state.acled_event_types),
            )
            st.session_state.selected_sub_event_types = st.multiselect(
                label="Select Sub Event(s)",
                options=sorted(st.session_state.acled_sub_event_types),
            )
            st.session_state.selected_disorder_types = st.multiselect(
                label="Select Disorder Type(s)",
                options=sorted(st.session_state.acled_disorder_types),
            )

        if actors_checkbox:
            st.session_state.selected_acled_actors = (
                st.session_state.acled_processor._get_actors_()
            )

        if event_types_checkbox:
            st.session_state.selected_event_types = (
                st.session_state.acled_processor._get_event_types_()
            )

        if sub_event_types_checkbox:
            st.session_state.selected_sub_event_types = (
                st.session_state.acled_processor._get_sub_event_types_()
            )

        if disorder_types_checkbox:
            st.session_state.selected_disorder_types = (
                st.session_state.acled_processor._get_disorder_types_()
            )

        update_acled_data(
            actors=st.session_state.selected_acled_actors,
            disorder_types=st.session_state.selected_disorder_types,
            event_types=st.session_state.selected_event_types,
            sub_event_types=st.session_state.selected_sub_event_types,
        )

# Process CELLEX Data
if st.session_state.CELLEX_FILES:
    initialize_cellex_variables()
    cellex_filter_expander = st.expander("Select CELLEX Filters Here")

    with cellex_filter_expander:
        cellex_checkbox_col, cellex_multi_select_col = st.columns([0.2, 0.8])

        with cellex_checkbox_col:
            cellex_checkbox = st.checkbox(
                f"Select all Cellex Actors",
                value=True,
            )

        with cellex_multi_select_col:
            selected_cellex_actors = st.multiselect(
                label="Select Cellex Actor(s)",
                options=st.session_state.cellex_processor._get_actors_(),
            )
        if cellex_checkbox:
            st.session_state.selected_cellex_actors = (
                st.session_state.cellex_processor._get_actors_()
            )

    update_cellex_data(actors=st.session_state.selected_cellex_actors)

# BYOD - Build Your Own Dashboard
if (
    "acled_data" in st.session_state
    or "cellex_data" in st.session_state
    or "gdelt_data" in st.session_state
):

    if st.button("Build Your Own Dashboard!"):

        # Ensure that we pass None for missing data
        acled_data = (
            st.session_state.acled_data if "acled_data" in st.session_state else None
        )
        gdelt_data = (
            st.session_state.gdelt_data if "gdelt_data" in st.session_state else None
        )
        cellex_data = (
            st.session_state.cellex_data if "cellex_data" in st.session_state else None
        )

        # Update map based on available data
        newmap = st.session_state.map_generator._reinitialize_map_(
            acled_data=acled_data,
            gdelt_data=gdelt_data,
            cellex_data=cellex_data,
        )

        # Display the map
        folium_static(newmap, width=2000, height=500)

        # st.markdown("Time Distribution")
        if "acled_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("View Time Distribution"):
                daily_line, monthly_line, yearly_line = st.columns(3)
                with daily_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            acled_data, "event_date", freq="daily"
                        )
                    )
                with monthly_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            acled_data, "event_date", freq="monthly"
                        )
                    )
                with yearly_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            acled_data, "event_date", freq="yearly"
                        )
                    )

        # Display Plots
        if "acled_data" in st.session_state and "plot_generator" in st.session_state:

            with st.expander("View Plots"):
                st.markdown("Type Distributions")
                event_pie, sub_event_pie, disorder_type = st.columns(3)
                with event_pie:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_pie_chart(
                            acled_data, "event_type"
                        )
                    )
                with sub_event_pie:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_pie_chart(
                            acled_data, "sub_event_type"
                        )
                    )
                with disorder_type:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_pie_chart(
                            acled_data, "disorder_type"
                        )
                    )

        # Display Timeline
        if "acled_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("Timeline"):
                st.session_state.plot_generator._plot_timeline_(
                    df=st.session_state.acled_data, datetime_column="event_date"
                )
        # Display Data
        with st.expander("Raw Data"):
            if acled_data is not None:
                st.markdown("Acled Data")
                st.dataframe(acled_data)
            if gdelt_data is not None:
                st.markdown("Gdelt Data")
                st.dataframe(gdelt_data)
            if cellex_data is not None:
                st.markdown("Cellex Data")
                st.dataframe(cellex_data)
