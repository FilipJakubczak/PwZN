from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DataRange1d, Select
from bokeh.plotting import figure
from bokeh.layouts import column, row
from os.path import dirname, join
import pandas as pd

def dataset(source, country):
    data = source[source["location"] == country].copy()
    
    data["date"] = pd.to_datetime(data["date"])

    return ColumnDataSource(data=data)

def make_plot(source, title):
    plot = figure(x_axis_type="datetime", width=800, tools="", toolbar_location=None)
    plot.title.text = title

    plot.line("date", "people_fully_vaccinated_per_hundred", source=source)

    # fixed attributes
    plot.xaxis.axis_label = None
    plot.yaxis.axis_label = "Total Vaccinations"
    plot.axis.axis_label_text_font_style = "bold"
    plot.x_range = DataRange1d(range_padding=0.0)
    plot.grid.grid_line_alpha = 0.3

    return plot

def update_plot(attrname, old, new):
    country = country_select.value
    plot.title.text = "People fully vaccinated per hundred people " + countries[country]

    src = dataset(data, countries[country])
    source.data.update(src.data)


country = "Poland"

data = pd.read_csv(join(dirname(__file__), 'vaccinations.csv'))
countries = dict(zip(data["location"], data["location"]))

country_select = Select(value=country, title='Country', options=sorted(countries))

source = dataset(data, countries[country])
plot = make_plot(source, "People fully vaccinated per hundred people for {}".format(countries[country]))

country_select.on_change("value", update_plot)

controls = column(country_select)

curdoc().add_root(row(plot, controls))
curdoc().title = "People fully vaccinated per hundred people"