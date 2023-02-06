# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 13:13:13 2022

@author: nimachuca
"""

import folium
import pandas as pd

## Tecnologias 

techs = [
    {"filename": "./data_chile/bess.xlsx", "name": "BESS", "color": "#a32727"},
    {"filename": "./data_chile/pv+bess.xlsx", "name": "PV+BESS", "color": "#525354"},
]

# Color 
#"#a32727" = red
#"#525354" = grey 


# Cuadro de informacion 

def popup_text(mastr_id, storage_unit, technology_name):
    return (
        f"<b>Name:</b> {storage_unit['Name']}<br>"
        f"<b>Status:</b> {storage_unit['Status']}<br>"
        f"<b>Power:</b> {round(storage_unit['Power']/1000, 1)} MW<br>"
        f"<b>E/P:</b> {round(storage_unit['E_to_P'], 1)}<br>"
        f"<b>Owner:</b> {storage_unit['Owner']}<br>"
        f"<b>Technology:</b> {technology_name}<br>"
        f"<b>Link:</b> {link}<br>"

    )

## Prepara la tabla 
def prepare_data():
    """
    drops projects from abroad (e.g. LU, AT) and without location
    drops erroneous household projects
    drops decommissioned projects
    renames some German lingo
    """

    data = pd.read_excel(tech["filename"], header=0, index_col=0)
    data.dropna(subset=["Location"], inplace=True)   # Elimina los que no tienen ubicaciom
    data.dropna(subset=["Latitude"], inplace=True)
    data.dropna(subset=["Longitude"], inplace=True)
    data.sort_values(by="Power", ascending=False, inplace=True)
    data['E_to_P'] = data["Capacity"] / data["Power"]
    return data

# MAPA 
def plot_battery_locations(map):
    for idx, item in data.iterrows():
        folium.Circle(
            location=[item["Latitude"],item["longitude"],],
            radius=item["Power"],
            popup=folium.Popup(html=popup_text(idx, item, tech["name"]), max_width="500"),
            color=tech["color"],
            fill_color=tech["color"],
            fill=True,
        ).add_to(map)

if __name__ == '__main__':
    battery_map = folium.Map(location=[-31.6, -70.1], zoom_start=5)
    for tech in techs:
        data = prepare_data()
        plot_battery_locations(battery_map)
    battery_map.save("battery_map_chile2.html")




