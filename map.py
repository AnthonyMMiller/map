import folium
import pandas

#Turn text file into list and then usable variables using pandas
data = pandas.read_csv("volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])

# Color selection for icon based on elevation
def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'

# Folium Map initial build
map = folium.Map(location=[38.58, -99.09], zoom_start=6, tiles="Stamen Toner")

# Initiate volcano feature group
fgv = folium.FeatureGroup(name="Volcanoes")

# Loop through list and add volcano location layer to map
for lt, ln, el in zip(lat,lon, elev):
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius = 7, popup=str(el)+"m", fill_color=color_producer(el), color = 'grey', fill= True, fill_opacity=0.7))

# Initiate population feature group
fgp = folium.FeatureGroup(name="population")

# Add Polygon Layer with colors; based on 2005 population size; from Json data
fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), 
style_function = lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000
else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000
else 'red'}))

# add feature groups to map
map.add_child(fgv)
map.add_child(fgp)
# add layer control panel
map.add_child(folium.LayerControl())
# save map
map.save("map1.html")

