from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from motion_detector import df

# add columns with valid time format
df["Start_string"] = df["Start"].dt.strftime("%H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%H:%M:%S")

cds = ColumnDataSource(df)

plot = figure(x_axis_type="datetime", height=100, width=500, sizing_mode="scale_width", title="Motion plot")
plot.yaxis.minor_tick_line_color = None
plot.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Start", "@Start_string"), ("End", "@End_string")])
plot.add_tools(hover)

quad = plot.quad(left="Start", right="End", bottom=0, top=1, color="green", source=cds)

output_file("Plot.html")
show(plot)

