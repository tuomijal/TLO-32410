import numpy as np
import pandas as pd
import geopy.distance

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.plotting import figure


def fetch_data():
    """

    """
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
        distance = distance.vincenty(catalonia_square_coords, apartment_coords).km
        return distance

    ld['distance_from_catalonia_square'] = ld[['latitude', 'longitude']].apply(get_distance, raw=True, axis=1)

    # dropna
    ld = ld.dropna(subset=['deal_index'])

    return ld

source = ColumnDataSource(data=dict(x=[], y=[])


p = figure(plot_height=600, plot_width=700, title="", toolbar_location=None, sizing_mode="scale_both")
p.circle(x="x", y="y", source=source)

l = column(p)

curdoc().add_root(l)

data = fetch_data()

source.data = dict(
    x=data.distance_from_catalonia_square,
    y=data.price_log)
