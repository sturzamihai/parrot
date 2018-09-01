import flask
import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import bridge_controller as bc
import numpy as np

X_temp = deque(maxlen=20)
X_temp.append(1)
Y_temp = deque(maxlen=20)

X_pres = deque(maxlen=20)
X_pres.append(1)
Y_pres = deque(maxlen=20)

X_humi = deque(maxlen=20)
X_humi.append(1)
Y_humi = deque(maxlen=20)

X_conc = deque(maxlen=20)
X_conc.append(1)
Y_conc = deque(maxlen=20)

app = dash.Dash(__name__, processes=4)

def get_stats(X):
    min = str(round(np.min(X), 2))
    max = str(round(np.max(X), 2))
    std = str(round(np.std(X), 2))
    avg = str(round(np.mean(X), 2))
    med = str(round(np.median(X), 2))
    return min, max, std, avg, med

app.layout = html.Div(
    [
        html.Div([
            html.Img(src="https://i.imgur.com/ihOBYtR.png",style={"display":"block","width":125,"margin":"auto auto"}),
            html.H2('Particle Accelerator Observation Tool',style={"display":"inline-block"})
        ],style={"border-right":"2px solid blue"}),
        html.Div([
            html.Div([
                html.Img(id="cam",src="http://192.168.162.254:10000/cgi-bin/video.cgi?msubmenu=mjpg",width="600",height="500",style={"display":"block"}),
                html.Img(id="usbcam",src="http://127.0.0.1:8081",width="600",height="500")
            ]),
            html.Div([
                html.P('Stats here', id='live-graph-stats'),
                dcc.Graph(id='live-graph',style={"height":250},config={'displayModeBar':False}),
                html.P('Stats here', id='live-graph-stats2'),
                dcc.Graph(id='live-graph2',style={"height":250},config={'displayModeBar':False}),
                html.P('Stats here', id='live-graph-stats3'),
                dcc.Graph(id='live-graph3',style={"height":250},config={'displayModeBar':False}),
                html.P('Stats here', id='live-graph-stats4'),
                dcc.Graph(id='live-graph4',style={"height":250},config={'displayModeBar':False}),
                dcc.Interval(
                    id='graph-update',
                    interval=2*1000
                )
            ])
        ],style={"padding":20,"display":"grid","grid-template-columns":"auto auto"}),

    ],style={"display":"grid","grid-template-columns":"225px auto"})

@app.callback(Output('live-graph', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    response = bc.analog_read_pin('rtua', 0)
    X_temp.append(X_temp[-1]+1)
    Y_temp.append(response)
    data = plotly.graph_objs.Scatter(
            x=list(X_temp),
            y=list(Y_temp),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data]}

@app.callback(
    Output('live-graph-stats', 'children'),
    events=[Event('graph-update', 'interval')])
def display_stats():
    stats = get_stats(Y_temp)
    stats_string = 'Stats for last 20 samples:\n'+ \
        'min: '+stats[0]+'\nmax: '+stats[1]+'\nstd: '+stats[2]+'\navg: '+stats[3]+'\nmed: '+stats[4]
    print(stats_string)
    return stats_string


@app.callback(Output('live-graph2', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    response = bc.analog_read_pin('rtua', 1)
    X_pres.append(X_pres[-1]+1)
    Y_pres.append(response)
    data = plotly.graph_objs.Scatter(
            x=list(X_pres),
            y=list(Y_pres),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data]}

@app.callback(
    Output('live-graph-stats2', 'children'),
    events=[Event('graph-update', 'interval')])
def display_stats():
    stats = get_stats(Y_pres)
    stats_string = 'Stats for last 20 samples:\n'+ \
        'min: '+stats[0]+'\nmax: '+stats[1]+'\nstd: '+stats[2]+'\navg: '+stats[3]+'\nmed: '+stats[4]
    print(stats_string)
    return stats_string

@app.callback(Output('live-graph3', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    response = bc.analog_read_pin('rtub', 0)
    X_humi.append(X_humi[-1]+1)
    Y_humi.append(response)
    data = plotly.graph_objs.Scatter(
            x=list(X_humi),
            y=list(Y_humi),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data]}

@app.callback(
    Output('live-graph-stats3', 'children'),
    events=[Event('graph-update', 'interval')])
def display_stats():
    stats = get_stats(Y_humi)
    stats_string = 'Stats for last 20 samples:\n'+ \
        'min: '+stats[0]+'\nmax: '+stats[1]+'\nstd: '+stats[2]+'\navg: '+stats[3]+'\nmed: '+stats[4]
    print(stats_string)
    return stats_string

@app.callback(Output('live-graph4', 'figure'),
              events=[Event('graph-update', 'interval')])
def update_graph_scatter():
    response = bc.analog_read_pin('rtub', 1)
    X_conc.append(X_conc[-1]+1)
    Y_conc.append(response)
    data = plotly.graph_objs.Scatter(
            x=list(X_conc),
            y=list(Y_conc),
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data]}

@app.callback(
    Output('live-graph-stats4', 'children'),
    events=[Event('graph-update', 'interval')])
def display_stats():
    stats = get_stats(Y_conc)
    stats_string = 'Stats for last 20 samples:\n'+ \
        'min: '+stats[0]+'\nmax: '+stats[1]+'\nstd: '+stats[2]+'\navg: '+stats[3]+'\nmed: '+stats[4]
    print(stats_string)
    return stats_string

if __name__ == '__main__':
    app.run_server(debug=True)
