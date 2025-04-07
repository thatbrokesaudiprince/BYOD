from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import streamlit as st


class CELLEXProcessor:

    def __init__(self, CELLEX_FILES):
        """Initialize the CELLEXProcessor class."""

        self.latlon_columns = ["Latitude", "Longitude"]
        self.data = self._store_data_(CELLEX_FILES)

    def _is_lat_lon(self, col_name: str) -> bool:
        """
        Check if the Cellex file contains lat-lon data (i.e., `col_name`
        is in `LATLON_COLUMNS`).

        Parameters
        ----------
        col_name : str
            The Cellex data column.

        Returns
        -------
        bool
            If _is_lat_lon is True, then we can use the file for
            visualization.
        """

        return col_name.strip().capitalize() in self.latlon_columns

    def _store_data_(self, CELLEX_FILES: list) -> dict[str, dict[str, list]]:
        cellex_data = {}
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._process_cellex_data, cellex_file)
                for cellex_file in CELLEX_FILES
            ]
            for future in as_completed(futures):
                file_name, result = future.result()
                if isinstance(result, str) and result.startswith("error::"):
                    st.error(
                        f"Error reading {file_name.name}: {result.replace('error::', '')}"
                    )
                else:
                    cellex_data[file_name.name] = result
        return cellex_data

    def _get_actors_(self):
        return list(set(self.data.keys()))

    def _get_meta_data_(self, cellexs: list = None) -> pd.DataFrame:
        """Return a subset of the data which matches the selected cellexs in a DataFrame."""

        if not self.data:
            return pd.DataFrame()
        else:
            filtered_metadata = []
            for cellex in cellexs:
                metadata = self.data[cellex].get("metadata")
                filtered_metadata.extend(metadata)
            return pd.DataFrame(filtered_metadata)

    def _filter_cellex_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter DataFrame and return only rows that contain lat-lon data."""

        filters = []
        if all(col in df.columns for col in self.latlon_columns):
            filters.append("Latitude")
            filters.append("Longitude")

        try:
            if filters:
                filtered_df = df.copy()
                filtered_df = filtered_df[filtered_df[filters].notna().all(axis=1)]
            else:
                filtered_df = pd.DataFrame([])
        except Exception as e:
            print(f"Something wrong with processing Cellex df: {e}")
            filtered_df = pd.DataFrame([])  # Return empty DataFrame if there is error
        return filtered_df

    def _process_cellex_data(self, cellex_file: str) -> dict[str, list]:
        """Process Cellex data (i.e., has lat-lon data)."""

        # Read data
        excel_file = pd.read_excel(cellex_file, sheet_name=None, header=1)

        # For mapping of filenames to metadata/lat-lon data
        processed_data = {
            "metadata": [],
            "lat_lons": [],
        }

        # Cellex data has sheet to DataFrame key-value mapping
        for sheet in excel_file.keys():
            # Get DataFrame
            df = excel_file[sheet]

            # Process if it has lat-lon data
            if any(self._is_lat_lon(col) for col in df.columns):
                # Filter only rows with lat-lon data
                filtered_df = self._filter_cellex_df(df)
                if not filtered_df.empty:
                    # Provide a sheet source key (e.g., "Locations")
                    filtered_df.loc[:, "CMD sheet name"] = sheet
                    filtered_df.loc[:, "CMD file name"] = cellex_file.name

                    # Convert to JSON-like/dictionary format
                    filtered_data_dicts = filtered_df.to_dict(orient="records")
                    lat_lons = [
                        (data_dict["Latitude"], data_dict["Longitude"])
                        for data_dict in filtered_data_dicts
                    ]

                    # Append metadata/lat-lon data
                    processed_data["metadata"].extend(filtered_data_dicts)
                    processed_data["lat_lons"].extend(lat_lons)
        return cellex_file, processed_data
