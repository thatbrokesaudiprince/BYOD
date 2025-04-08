import streamlit as st
from streamlit_folium import folium_static
import pandas as pd
import plotly.express as px
from utils import *

# Import utility functions

# Set page layout
st.set_page_config(layout="wide", page_title="Build Your Own Dashboard")
st.title("Welcome to Build Your Own Dashboard🖥️!")
st.subheader(
    "A CEM|ACLED|GDELT Analysis platform developed by Analysts for Analysts📈💰📊"
)
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
        label="Upload GDELT data here!",
        accept_multiple_files=True,
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
            st.session_state.selected_acled_actors = st.multiselect(
                label="Select Actor(s)", options=sorted(st.session_state.acled_actors)
            )
            st.session_state.selected_acled_event_types = st.multiselect(
                label="Select Event(s)",
                options=sorted(st.session_state.acled_event_types),
            )
            st.session_state.selected_acled_sub_event_types = st.multiselect(
                label="Select Sub Event(s)",
                options=sorted(st.session_state.acled_sub_event_types),
            )
            st.session_state.selected_acled_disorder_types = st.multiselect(
                label="Select Disorder Type(s)",
                options=sorted(st.session_state.acled_disorder_types),
            )

        if actors_checkbox:
            st.session_state.selected_acled_actors = (
                st.session_state.acled_processor._get_actors_()
            )

        if event_types_checkbox:
            st.session_state.selected_acled_event_types = (
                st.session_state.acled_processor._get_event_types_()
            )

        if sub_event_types_checkbox:
            st.session_state.selected_acled_sub_event_types = (
                st.session_state.acled_processor._get_sub_event_types_()
            )

        if disorder_types_checkbox:
            st.session_state.selected_acled_disorder_types = (
                st.session_state.acled_processor._get_disorder_types_()
            )

        acled_start_date_col, acled_end_date_col = st.columns(2)
        with acled_start_date_col:
            st.session_state.selected_acled_start_date = st.date_input(
                "Enter ACLED Start Date", value=None
            )
        with acled_end_date_col:
            st.session_state.selected_acled_end_date = st.date_input(
                "Enter ACLED End Date", value=None
            )

        update_acled_data(
            start_date=pd.to_datetime(st.session_state.selected_acled_start_date),
            end_date=pd.to_datetime(st.session_state.selected_acled_end_date),
            actors=st.session_state.selected_acled_actors,
            disorder_types=st.session_state.selected_acled_disorder_types,
            event_types=st.session_state.selected_acled_event_types,
            sub_event_types=st.session_state.selected_acled_sub_event_types,
        )


# Process GDELT Data
if len(st.session_state.GDELT_FILES) > 0:
    initialize_gdelt_variables()

    gdelt_filter_expander = st.expander("Select GDELT Filters Here")

    with gdelt_filter_expander:
        checkbox_col, multi_select_col = st.columns([0.2, 0.8])

        with checkbox_col:
            persons_checkbox = st.checkbox(
                f"Select all Persons",
                value=True,
            )
            organizations_checkbox = st.checkbox(
                f"Select all Organizations", value=True
            )
            other_mentions_checkbox = st.checkbox(
                f"Select all Other Mentions", value=True
            )
            sources_checkbox = st.checkbox(f"Select all Sources", value=True)
            countries_checkbox = st.checkbox(f"Select all Countries", value=True)

        with multi_select_col:
            st.session_state.selected_gdelt_persons = st.multiselect(
                label="Select Person(s)", options=sorted(st.session_state.gdelt_persons)
            )
            st.session_state.selected_gdelt_organizations = st.multiselect(
                label="Select Organization(s)",
                options=sorted(st.session_state.gdelt_organizations),
            )
            st.session_state.selected_gdelt_other_mentions = st.multiselect(
                label="Select Other Mention(s)",
                options=sorted(st.session_state.gdelt_other_mentions),
            )
            st.session_state.selected_gdelt_sources = st.multiselect(
                label="Select Source(s)",
                options=sorted(st.session_state.gdelt_sources),
            )
            st.session_state.selected_gdelt_countries_states = st.multiselect(
                label="Select Countries",
                options=sorted(st.session_state.gdelt_countries_states),
            )

        if other_mentions_checkbox:
            st.session_state.selected_gdelt_other_mentions = (
                st.session_state.gdelt_processor._get_other_mentions_()
            )

        if sources_checkbox:
            st.session_state.selected_gdelt_sources = (
                st.session_state.gdelt_processor._get_sources_()
            )

        if persons_checkbox:
            st.session_state.selected_gdelt_persons = (
                st.session_state.gdelt_processor._get_persons_()
            )

        if countries_checkbox:
            st.session_state.selected_gdelt_countries = (
                st.session_state.gdelt_processor._get_countries_states_()
            )

        if organizations_checkbox:
            st.session_state.selected_gdelt_organizations = (
                st.session_state.gdelt_processor._get_organizations_()
            )

        gdelt_start_date_col, gdelt_end_date_col = st.columns(2)
        with gdelt_start_date_col:
            st.session_state.selected_gdelt_start_date = st.date_input(
                "Enter GDELT Start Date", value=None
            )
        with gdelt_end_date_col:
            st.session_state.selected_gdelt_end_date = st.date_input(
                "Enter GDELT End Date", value=None
            )
        update_gdelt_data(
            persons=st.session_state.selected_gdelt_persons,
            organizations=st.session_state.selected_gdelt_organizations,
            countries_states=st.session_state.selected_gdelt_countries_states,
            sources=st.session_state.selected_gdelt_sources,
            other_mentions=st.session_state.selected_gdelt_other_mentions,
            start_date=pd.to_datetime(st.session_state.selected_gdelt_start_date),
            end_date=pd.to_datetime(st.session_state.selected_gdelt_end_date),
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
            with st.expander("View ACLED Time Distribution"):
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
        if "gdelt_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("View GDELT Time Distribution"):
                daily_line, monthly_line, yearly_line = st.columns(3)
                with daily_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            gdelt_data, "event_date", freq="daily"
                        )
                    )
                with monthly_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            gdelt_data, "event_date", freq="monthly"
                        )
                    )
                with yearly_line:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_time_series(
                            gdelt_data, "event_date", freq="yearly"
                        )
                    )

        # Display Plots
        if "acled_data" in st.session_state and "plot_generator" in st.session_state:

            with st.expander("ACLED Plots"):
                st.markdown("ACLED Type Distributions")
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

        if "gdelt_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("GDELT Plots"):
                st.markdown("GDELT Distributions")
                persons_col, organizations_col = st.columns(2)
                with persons_col:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_gdelt_pie_chart(
                            st.session_state.gdelt_data, "Mentioned Persons"
                        )
                    )
                with organizations_col:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_gdelt_pie_chart(
                            st.session_state.gdelt_data, "Mentioned Organizations"
                        )
                    )

                # # with om_col:
                # st.plotly_chart(
                #     st.session_state.plot_generator.plot_gdelt_pie_chart(
                #         st.session_state.gdelt_data, "Other Mentions"
                #     )
                # )
                countries_col, sources_col = st.columns(2)
                with countries_col:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_gdelt_pie_chart(
                            st.session_state.gdelt_data, "Mentioned Countries/States"
                        )
                    )
                with sources_col:
                    st.plotly_chart(
                        st.session_state.plot_generator.plot_gdelt_pie_chart(
                            st.session_state.gdelt_data, "Source"
                        )
                    )

        # Display Timeline
        if "acled_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("ACLED Timeline"):
                st.session_state.plot_generator._plot_acled_timeline_(
                    df=st.session_state.acled_data, datetime_column="event_date"
                )
        if "gdelt_data" in st.session_state and "plot_generator" in st.session_state:
            with st.expander("GDELT Timeline"):
                st.session_state.plot_generator._plot_gdelt_timeline_(
                    df=st.session_state.gdelt_data, datetime_column="event_date"
                )

        # # Display Data
        with st.expander("Raw Data"):
            if "acled_data" in st.session_state:
                st.markdown("Acled Data")
                st.dataframe(acled_data)
            if "gdelt_data" in st.session_state:
                st.markdown("Gdelt Data")
                st.dataframe(st.session_state.gdelt_data)
            if "cellex_data" in st.session_state:
                st.markdown("Cellex Data")
                st.dataframe(cellex_data)
