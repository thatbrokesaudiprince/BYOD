import folium
import pandas as pd
import branca
from folium.plugins import GroupedLayerControl
import os
import streamlit as st

# Get the absolute path for your images directory
images_dir = os.path.join(os.getcwd(), "frontend", "images")


class MapGenerator:

    def __init__(self, tiles: str, attr: str, zoom_start: int = 6):
        self.ACLED_BATTLE_layer = folium.FeatureGroup(name="ACLED BATTLES", show=True)
        self.ACLED_PROTEST_layer = folium.FeatureGroup(name="ACLED PROTESTS", show=True)
        self.ACLED_RIOT_layer = folium.FeatureGroup(
            name="ACLED RIOTS", show=True, control=True
        )
        self.ACLED_EXPLOSION_layer = folium.FeatureGroup(
            name="ACLED EXPLOSION/REMOTE VIOLENCE", show=True, control=True
        )
        self.ACLED_VIOLENCE_layer = folium.FeatureGroup(
            name="ACLED VIOLENCE AGAINST CIVILLIANS", show=True, control=True
        )
        self.ACLED_STRATEGIC_layer = folium.FeatureGroup(
            name="ACLED STRATEGIC DEVELOPMENTS", show=True, control=True
        )
        self.GDELT_LAYER = folium.FeatureGroup(name="GDELT", show=True, control=True)

        # self.GDELT_layer = folium.FeatureGroup(name="GDELT")
        self.CELLEX_LAYER = folium.FeatureGroup(name="CELLEX", show=True, control=True)

        # Modify the icon map to use absolute paths
        self.icon_map = {
            "Battles": os.path.join(images_dir, "battle_icon.png"),
            "Protests": os.path.join(images_dir, "protest_icon.png"),
            "Riots": os.path.join(images_dir, "riot_icon.png"),
            "Explosions/Remote violence": os.path.join(images_dir, "bomb_icon.png"),
            "Violence against civilians": os.path.join(images_dir, "violence_icon.png"),
            "Strategic developments": os.path.join(images_dir, "strategy_icon.png"),
            "CELLEX": os.path.join(images_dir, "device_icon.png"),
            "GDELT": os.path.join(images_dir, "gdelt_icon.png"),
        }

        self.acled_event_layer_map = {
            "Battles": self.ACLED_BATTLE_layer,
            "Protests": self.ACLED_EXPLOSION_layer,
            "Riots": self.ACLED_PROTEST_layer,
            "Explosions/Remote violence": self.ACLED_EXPLOSION_layer,
            "Violence against civilians": self.ACLED_VIOLENCE_layer,
            "Strategic developments": self.ACLED_STRATEGIC_layer,
        }

        self.map = folium.Map(tiles=tiles, attr=attr, zoom_start=zoom_start)

    def _insert_marker_to_layer(
        self, marker: folium.Marker, layer: folium.FeatureGroup
    ) -> None:
        """Assigns a marker to a layer"""

        marker.add_to(layer)

    def _generate_gdelt_markers_(self, gdelt_data: pd.DataFrame):
        """Generate the markers for gdelt data and add it to the gdelt map layer"""
        for index, row in gdelt_data.iterrows():
            event_date = row["event_date"]
            notes = row["Headline"]
            mp = row["Mentioned Persons"]
            mo = row["Mentioned Organizations"]
            cat = row["Categories"]
            source_and_link = row["Source"] + " | " + row["link"]
            popup = f"""
            <div style="font-family: Arial, sans-serif; padding: 5px;">
                <p><strong>Date of News:</strong> {event_date}</p>
                <p><strong>Headline: {notes}</strong> </p>
                <p><strong>Mentioned People:</strong></p>
                <p>{mp}</p>
                <p><strong>Mentioned Organizations:</strong></p>
                <p>{mo}</p>
                <p><strong>Tagged Categories:</strong></p>
                <p>{cat}</p>
                <p><strong>References:</strong> {source_and_link}</p>
            </div>
            """
            print(row)
            for point in row["location"].split(", "):
                location = (
                    float(point.replace("(", "").replace(")", "").split(" ")[2]),
                    float(point.replace("(", "").replace(")", "").split(" ")[1]),
                )
                marker = self._create_marker_(
                    tooltip=notes,
                    location=location,
                    icon=self.icon_map["GDELT"],
                    icon_color="red",
                    color="red",
                    popup=popup,
                )

                self._insert_marker_to_layer(marker=marker, layer=self.GDELT_LAYER)

    def _generate_acled_markers_(self, acled_data: pd.DataFrame):
        for index, row in acled_data.iterrows():
            main_actor = (
                str(row["actor1"])
                + ";  "
                + str(row["actor2"])
                + "  |  "
                + str(row["event_type"])
            )
            event_date = row["event_date"]
            event_type = str(row["event_type"])
            disorder_type = str(row["disorder_type"])
            sub_event_type = str(row["sub_event_type"])
            notes = str(row["notes"])
            location = (float(row["latitude"]), float(row["longitude"]))
            source_and_scale = row["source"] + "; " + row["source_scale"]

            popup = f"""
            <div style="font-family: Arial, sans-serif; padding: 5px;">
                <p><strong>Date of Event:</strong> {event_date}</p>
                <p><strong>Event Type:</strong> {disorder_type}; {event_type}; {sub_event_type}</p>
                <p><strong>Location:</strong> {location}</p>
                <p><strong>Event Notes:</strong></p>
                <p>{notes}</p>
                <p><strong>References:</strong> {source_and_scale}</p>
            </div>
            """
            marker = self._create_marker_(
                tooltip=main_actor,
                location=location,
                icon=self.icon_map[row["event_type"]],
                icon_color="red",
                color="red",
                popup=popup,
            )

            self._insert_marker_to_layer(
                marker=marker, layer=self.acled_event_layer_map[event_type]
            )

    def _generate_cellex_markers_(self, cellex_data: pd.DataFrame):
        for index, row in cellex_data.iterrows():
            # Extracting the relevant data for each cellex
            main_actor = str(row["CMD file name"])
            location = (float(row["Latitude"]), float(row["Longitude"]))
            popup = """<div style="font-family: Arial, sans-serif; padding: 5px;">"""
            row_dict = row.to_dict()
            for col, val in row_dict.items():
                if col in ["CMD file name"]:
                    continue
                popup += f"<p><strong>{col}:</strong>{val}</p>"
            popup += "</div>"

            marker = self._create_marker_(
                tooltip=main_actor,
                location=location,
                icon=self.icon_map["CELLEX"],
                icon_color="blue",
                color="blue",
                popup=popup,
            )
            self._insert_marker_to_layer(marker=marker, layer=self.CELLEX_LAYER)

    def _create_marker_(
        self,
        tooltip: str,
        location: tuple,
        icon: str,
        icon_color: str,
        color: str,
        popup: str,
    ) -> folium.Marker:
        customicon = folium.CustomIcon(
            icon_image=icon, icon_size=(20, 20), icon_anchor=(10, 10)
        )
        iframe = branca.element.IFrame(
            html=popup, width=300, height=200
        )  # Adjust dimensions as needed

        return folium.Marker(
            location=location,
            tooltip=tooltip,
            icon=customicon,
            popup=folium.Popup(
                iframe, parse_html=True, max_width=300
            ),  # Adjust max_width if needed
        )

    def _reinitialize_map_(
        self,
        acled_data: pd.DataFrame = None,
        gdelt_data: pd.DataFrame = None,
        cellex_data: pd.DataFrame = None,
    ):
        if acled_data is not None and not acled_data.empty:
            self._generate_acled_markers_(acled_data)

        if gdelt_data is not None and not gdelt_data.empty:
            self._generate_gdelt_markers_(gdelt_data=gdelt_data)
            pass

        if cellex_data is not None and not cellex_data.empty:
            self._generate_cellex_markers_(cellex_data=cellex_data)

        # Create a template group to fill in
        groups = {"ACLED": [], "GDELT": [], "CELLEX": []}

        layers = [
            self.ACLED_BATTLE_layer,
            self.ACLED_EXPLOSION_layer,
            self.ACLED_PROTEST_layer,
            self.ACLED_RIOT_layer,
            self.ACLED_VIOLENCE_layer,
            self.ACLED_STRATEGIC_layer,
            self.GDELT_LAYER,
            self.CELLEX_LAYER,
        ]
        #  Add the layer into the map if there are markers
        for layer in layers:
            if len(layer._children.keys()) > 0:
                self.map.add_child(layer)
                if "ACLED" in layer.layer_name:
                    groups["ACLED"].append(layer)
                if "GDELT" in layer.layer_name:
                    groups["GDELT"].append(layer)
                if "CELLEX" in layer.layer_name:
                    groups["CELLEX"].append(layer)

        # Add LayerControl to the map after all layers are added
        folium.LayerControl(collapsed=False).add_to(self.map)

        # Add GroupedLayerControl to filter the layers on the map (layer toggle)
        GroupedLayerControl(
            groups=groups,
            exclusive_groups=False,
            collapsed=False,
        ).add_to(self.map)

        return self.map
