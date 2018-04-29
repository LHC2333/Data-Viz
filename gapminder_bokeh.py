import pandas as pd
from bokeh.plotting import figure
from bokeh.layouts import column,widgetbox,row
from bokeh.models import ColumnDataSource,HoverTool,CategoricalColorMapper
from bokeh.models.widgets import Select,Slider
from bokeh.palettes import Spectral6
from bokeh.io import curdoc

#import data
gapminder = pd.read_csv(r'gapminder.csv',index_col='Year')

#setting up the date dimension
date_start = gapminder.index.values[0]
date_end = gapminder.index.values[-1]

#setting up hte source data
source = ColumnDataSource(data={
    'x'       : gapminder.loc[date_start].fertility,
    'y'       : gapminder.loc[date_start].life,
    'country' : gapminder.loc[date_start].Country,
    'pop'     : (gapminder.loc[date_start].population / 20000000) + 2,
	'gdp'     : gapminder.loc[date_start].gdp,
	'child mortality' : gapminder.loc[date_start].child_mortality,
    'region'  : gapminder.loc[date_start].region,

})

#setting up the xy range
xmin, xmax = min(gapminder.fertility), max(gapminder.fertility)
ymin, ymax = min(gapminder.life), max(gapminder.life)

#setting up the color for categorical data
regions_list = gapminder.region.unique().tolist()
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

#setting up the plot 
plot = figure(title='Life VS. Fertility WorldWide in 1964',
			  x_range=(xmin, xmax),
			  y_range=(ymin, ymax),
			  plot_width=800, 
			  plot_height=600)

			  
plot.circle(x = 'x', 
			y = 'y',
			fill_alpha=0.8,  
			source=source, 
			color=dict(field='region', transform=color_mapper),
			legend='region'
			)

#setting up the legend and the title			
plot.legend.label_text_font = "times"
plot.legend.location = 'bottom_left'
plot.legend.label_standoff = 1
plot.legend.glyph_height = 30
plot.legend.spacing = 1
plot.legend.padding = 5

plot.title.text_font_size = '16pt'
plot.title.align = 'center'

#setting up the xy dropdown
x_value = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x value'
)

y_value = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y value'
)

#setting up the hover tool
hover = HoverTool(tooltips=[('Country', '@country'),
							(x_value.value,'@x'),
							(y_value.value,'@y'),
							('GDP','@gdp'),
							('Child Mortality','@child_mortality')
							])

#defining the update function
def update_value(attr, old, new):

    yr = slider.value
    x = x_value.value
    y = y_value.value
	
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    new_data = {
        'x'       : gapminder.loc[yr][x],
		'y'       : gapminder.loc[yr][y],
		'country' : gapminder.loc[yr].Country,
		'pop'     : (gapminder.loc[yr].population / 20000000) + 2,
		'gdp'     : gapminder.loc[date_start].gdp,
		'child mortality' : gapminder.loc[date_start].child_mortality,
		'region'  : gapminder.loc[yr].region,
		}
    
    source.data = new_data

    
    plot.x_range.start = min(gapminder[x])
    plot.x_range.end = max(gapminder[x])
    plot.y_range.start = min(gapminder[y])
    plot.y_range.end = max(gapminder[y])

    
    plot.title.text = '%s VS. %s in %d' % (y,x,yr)

#setting up the slider
slider = Slider(start=date_start,end=date_end,step=1,value=date_start,title='Year')			

#making thing interactive using the update function
slider.on_change('value',update_value)  
x_value.on_change('value', update_value)
y_value.on_change('value', update_value)

plot.add_tools(hover)

layout = row(widgetbox(x_value,y_value,slider), plot)
curdoc().add_root(layout)
curdoc().title = "Sliders"