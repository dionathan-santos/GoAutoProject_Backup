import pydeck as pdk
import random

def assign_colors(dealerships):
    colors = {dealer: [random.randint(0, 255) for _ in range(3)] for dealer in dealerships["dealer_name"].unique()}
    dealerships["color"] = dealerships["dealer_name"].map(colors)
    return dealerships, colors

def create_pydeck_map(dealerships):
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=dealerships,
        get_position="[Longitude, Latitude]",
        get_fill_color="[color[0], color[1], color[2], 160]",
        get_radius=300,
        pickable=True,
    )
    view_state = pdk.ViewState(
        latitude=dealerships["Latitude"].mean(),
        longitude=dealerships["Longitude"].mean(),
        zoom=10,
    )
    return pdk.Deck(layers=[layer], initial_view_state=view_state)
