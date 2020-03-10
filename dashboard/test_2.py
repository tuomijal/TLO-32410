from bokeh.models import ColumnDataSource, ColorBar
from bokeh.plotting import figure, show, curdoc
from bokeh.io import output_file
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis

import pandas as pd

print("Loading data")
ld_backup = pd.read_csv(f"http://data.insideairbnb.com/spain/catalonia/barcelona/2020-02-16/data/listings.csv.gz")
ld = ld_backup.copy()

# convert price dtype
ld['price'] = ld.price.str[1:].replace("$", '')
ld['price'] = ld.price.str.replace(',', '')
ld['price'] = ld.price.astype(float)

# calculcate deal index
ld['deal_index'] = ld.review_scores_rating / ld.price

# instantiate mapper and source
ld_nona= ld.dropna(subset=['deal_index'])
psource = ColumnDataSource(ld_nona)
mapper = linear_cmap(field_name='deal_index', palette=Viridis[256], low=ld.deal_index.min(), high=ld.deal_index.max())

# plot
p = figure(title="A test", plot_width=1280, plot_height=1280, output_backend="webgl")
c = p.circle('longitude', 'latitude', source=psource, color=mapper, fill_alpha=0.7, size=12)

color_bar = ColorBar(color_mapper=mapper['transform'])
p.add_layout(color_bar, 'right')

curdoc().add_root(p)
