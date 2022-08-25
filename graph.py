from bokeh.plotting import figure
from bokeh.embed import components
import api


def get_graph_elements(coin, week, scenario, filter_list):

    # change get_hashrates_from_database to return percentages of total
    # make percentages the y_axis and have the hashrate as the label

    x_axis = []
    y_axis = []

    if scenario == 'solar':
        solar_lat = filter_list[0]  # 0,1,2,3
        graph_data = api.graph_mining_pool_hashrate(coin, week, solar_lat)
        x_axis = list(graph_data.keys())
        y_axis = [percentage[1] for percentage in list(graph_data.values())]
        if solar_lat == 0:
            y_axis_title = "Percentage of Total Hashrate"
        else:
            y_axis_title = "Percentage of Remaining Mining Pool's Hashrate"
    elif scenario == 'countries':
        countries = filter_list
        y_axis_title = "Percentage of Total Hashrate"

    # https://docs.bokeh.org/en/latest/docs/user_guide/plotting.html
    plot = figure(
        x_range=x_axis,
        width=400,
        height=400,
        toolbar_location=None)

    plot.vbar(x_axis,
              top=y_axis,
              width=0.5,
              bottom=0,
              color="firebrick")

    plot.sizing_mode = 'stretch_width'
    plot.xaxis.axis_label = "Mining Pools"
    plot.yaxis.axis_label = y_axis_title
    plot.xaxis.major_label_orientation = "vertical"

    return components(plot)
