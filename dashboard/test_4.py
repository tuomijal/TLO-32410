import sqlite3 as sql
from os.path import dirname, join

import numpy as np
import pandas as pd
import geopy.distance

from bokeh.io import curdoc
from bokeh.layouts import column, layout
from bokeh.models import ColumnDataSource, Div, Select, Slider, TextInput
from bokeh.plotting import figure
from bokeh.sampledata.movies_data import movie_path

ld_backup = pd.read_csv(f"http://data.insideairbnb.com/spain/catalonia/barcelona/2020-02-16/data/listings.csv.gz")
ld = ld_backup.copy()

# convert price dtype
ld['price'] = ld.price.str[1:].replace("$", '')
ld['price'] = ld.price.str.replace(',', '')
ld['price'] = ld.price.astype(float)

# log of price
ld['price_log'] = ld.price.apply(np.log)
ld['price_log'] = ld.price_log.replace([np.inf, -np.inf], np.nan)
ld['price_log'] = ld.price_log.fillna(value=0)


# calculcate deal index
ld['deal_index'] = ld.review_scores_rating / ld.price

# calculate distance from Plaza de Catalonia
def get_distance(apartment_coords):
    catalonia_square_coords = (41.386710, 2.169401)
    distance = geopy.distance.vincenty(catalonia_square_coords, apartment_coords).km
    return distance

ld['distance_from_catalonia_square'] = ld[['latitude', 'longitude']].apply(get_distance, raw=True, axis=1)

# dropna
ld = ld.dropna(subset=['deal_index'])

axis_map = {
    "Tomato Meter": "Meter",
    "Numeric Rating": "numericRating",
    "Number of Reviews": "Reviews",
    "Box Office (dollars)": "BoxOffice",
    "Length (minutes)": "Runtime",
    "Year": "Year",
}


# Create Input controls
reviews = Slider(title="Minimum number of reviews", value=80, start=10, end=300, step=10)
min_year = Slider(title="Year released", start=1940, end=2014, value=1970, step=1)
max_year = Slider(title="End Year released", start=1940, end=2014, value=2014, step=1)
oscars = Slider(title="Minimum number of Oscar wins", start=0, end=4, value=0, step=1)
boxoffice = Slider(title="Dollars at Box Office (millions)", start=0, end=800, value=0, step=1)
director = TextInput(title="Director name contains")
cast = TextInput(title="Cast names contains")
x_axis = Select(title="X Axis", options=sorted(axis_map.keys()), value="Tomato Meter")
y_axis = Select(title="Y Axis", options=sorted(axis_map.keys()), value="Number of Reviews")

# Create Column Data Source that will be used by the plot
source = ColumnDataSource(data=dict(x=[], y=[], color=[], title=[], year=[], revenue=[], alpha=[]))

TOOLTIPS=[
    ("Title", "@title"),
    ("Year", "@year"),
    ("$", "@revenue")
]

p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, tooltips=TOOLTIPS, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source, size=7, line_color=None, fill_alpha="alpha")


def select_data():
    selected = ld
    return selected


def update():
    df = select_data()
    x_name = "x"
    y_name = "y"

    p.xaxis.axis_label = "x"
    p.yaxis.axis_label = "y"
    p.title.text = "%d movies selected" % len(df)
    source.data = dict(
        x=df["distance_from_catalonia_square"],
        y=df["price"]
    )

controls = [reviews, boxoffice, min_year, max_year, oscars, director, cast, x_axis, y_axis]
for control in controls:
    control.on_change('value', lambda attr, old, new: update())

inputs = column(*controls, width=320, height=1000)
inputs.sizing_mode = "fixed"
l = layout([
    [inputs, p],
], sizing_mode="scale_both")

update()  # initial load of the data

curdoc().add_root(l)
curdoc().title = "Movies"
