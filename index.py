import dash
import dash_core_components as dcc
import dash_html_components as html
import time
from collections import deque
import plotly.graph_objs as go
import random


app = dash.Dash('greenhouse-data')

max_length = 20
times = deque(maxlen=max_length)
temperatura = deque(maxlen=max_length)
humedad = deque(maxlen=max_length)
luz = deque(maxlen=max_length)

data_dict = {"Temperatura": temperatura,
             "Humedad": humedad,
             "Luz": luz
}


def update_values(times,temperatura,humedad, luz):
    times.append(time.time())
    if len(times) == 1:
        temperatura.append(random.randrange(200,220))
        humedad.append(random.randrange(95,115))
        luz.append(random.randrange(190,215))
    else:
        for data_of_interest in [temperatura,humedad,luz]:
            data_of_interest.append(data_of_interest[-1]+data_of_interest[-1]*random.uniform(-0.0001,0.0001))
    return times, temperatura, humedad, luz

times, temperatura, humedad, luz = update_values(times, temperatura, humedad, luz)

app.layout = html.Div([
    html.Div([
        html.H2('Datos de Invernadero',
                style={'float':'left',
                       })


    ]),
    dcc.Dropdown(id='nombre-dato-invernadero',
                 options=[{'label': s, 'value': s}
                          for s in data_dict.keys()],
                 value=['Temperatura','Humedad','Luz'],
                 multi=True
                 ),
    html.Div(children=html.Div(id='graphs'), className='row'),
    dcc.Interval(
        id = 'graph-update',
        interval=100),
    ], className="container",style={'width':'98%','margin-left':10, 'margin-right':10,'max-width':50000})

@app.callback(
    dash.dependencies.Output('graphs','children'),
    [dash.dependencies.Input('nombre-dato-invernadero','value')],
    events=[dash.dependencies.Event('graph-update','interval')])

def update_graph(data_names):
    graphs=[]
    global times
    global temperatura
    global humedad
    global luz
    times, temperatura, humedad, luz = update_values(times,temperatura,humedad,luz)

    if len(data_names)>2:
        class_choice = 'col s12 m6 14'
    elif len(data_names) == 2:
        class_choice = 'col s12 m6 16'
    else:
        class_choice = 'col s12'

    for data_name in data_names:
        data = go.Scatter(
            x=list(times),
            y=list(data_dict[data_name]),
            name='Scatter',
            fill="tozeroy",
            fillcolor="#6897bb"
        )

        graphs.append(html.Div(dcc.Graph(
            id=data_name,
            animate=True,
            figure={'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(times), max(times)]),
                                                        yaxis=dict(range=[min(data_dict[data_name]),
                                                                          max(data_dict[data_name])]),
                                                        margin={'l': 50, 'r': 1, 't': 45, 'b': 1},
                                                        title='{}'.format(data_name))}
        ), className=class_choice))
    return graphs

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css"]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_css:
    app.scripts.append_script({'external_url': js})

if __name__ == '__main__':
    app.run_server(debug=True)
