import pandas as pd
import os
import itertools
import streamlit as st

# Get the absolute path for your images directory
# references_dir = os.path.join(os.getcwd(), "references")
# print(references_dir)
# cameo_txt = os.path.join(references_dir, "cameo.txt")
# cameo_codes = {}

# with open(cameo_txt, "r", encoding= "utf8") as f:
#     # read th text file line by line
#     lines = f.readlines()
#     for line in lines:
#         print(line)
#         code, desc = line.split(",")[0], line.split(",")[1:]
#         cameo_codes[code] = desc


# class GDELTProcessor:
#     def __init__(self,GDELT_FILES):

#     def _generate_cameo_dict_(self, cameo_file_path: str):


#     def _store_data_(self, GDELT_FILES: list) -> pd.DataFrame:
#         # Initialize empty dataframe to store all data
#         all_acled_data = pd.DataFrame()
#         # Iterated through mutliples files from streamlit file uploader
#         for file in GDELT_FILES:
#             # Read current file
#             current_file_data = pd.read_csv(file)
#             # Validate file
#             if list(current_file_data) == list(self.column_definition.keys()):
#                 # Concatenate data
#                 all_acled_data = pd.concat([current_file_data, all_acled_data])
#             else:
#                 st.info(
#                     f"Skipping {file} \nReason: does not conform to ACLED data format"
#                 )
#         all_acled_data.sort_values(by="event_date", ascending=True, inplace=True)
#         # return all data
#         return all_acled_data

#     def _get_columns_(self) -> list:
#         """Returns a list of all column names"""
#         return list(self.column_definition.keys())

#     def _get_definition_(self, col: str):
#         """Returns the definition of a column"""
#         return self.column_definition[col]

#     def _get_disorder_types_(self) -> list:
#         """Returns a list of all event types available"""
#         return list(self.data["disorder_type"].unique())

#     def _get_event_types_(self) -> list:
#         """Returns a list of all event types available"""
#         return list(self.data["event_type"].unique())

#     def _get_sub_event_types_(self) -> list:
#         """Returns a list of all event types available"""
#         return list(self.data["sub_event_type"].unique())

#     def _get_description_(self, event_id_cnty: str) -> str:
#         """Returns the event description note for a unique event"""
#         return self.data["note"][self.data["event_id_cnty"] == event_id_cnty]

#     def _get_actors_(self) -> list:
#         """Returns a list of all associated actors"""
#         cols = ["actor1", "assoc_actor_1", "actor2", "assoc_actor_2"]
#         actors = []

#         for col in cols:
#             temp = (
#                 self.data[col].dropna().unique()
#             )  # Remove NaN values and get unique actors
#             actors.append(temp.tolist())

#         result = set(
#             itertools.chain.from_iterable(actors)
#         )  # Flatten the list and remove duplicates
#         return list(
#             result
#         )  # Convert the set back to list if you need a list as a return type
