from math import pi

import pandas as pd

import bokeh.io
from bokeh.palettes import viridis
from bokeh.plotting import figure, output_file, save
from bokeh.transform import cumsum



def pieChart(df):
    bokeh.io.output_file('static/graphics/pie.html')
    labels=list(df['source'].unique())
    cant=list(df['source'].value_counts())
    x = {labels[i]: cant[i] for i in range(len(labels))}

    data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = viridis(len(x))

    p = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
               tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

    p.wedge(x=0, y=1, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color',legend_field='country', source=data)

    p.axis.axis_label=None
    p.axis.visible=False
    p.grid.grid_line_color = None
    # output_file('static/graphics/pie.html')
    return p