import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

# Young's modulus constant in Pascal
E = {
    'aluminum': 68.0 * 10**9,
    'wood': 10.0 * 10**9,
    'titanium': 116.0 * 10**9,
    'steel': 200.0 * 10**9,}

error_msg_a = 'Is a between 0 and L?'
error_msg_support_type = 'Invalid support_type'
error_msg_xsection = 'Invalid xsection'

# F: force magnitude in newtons. this is a float.
# x: inspection location, beam deflection at this location, in meters. this is a float.
# material: will affect E (Young's modulus). expected value: 'aluminum', 'wood', 'titanium', 'steel'
# xsection: beam cross section geometry in meters. will affect I. expected value: {'type': 'rectangular', 'b': float, 'h': float}, {'type': 'circle', 'r': float}
# a: force location from left end of beam in meters. this is a float.
# L: total length of beam in meters. this is a float.
# support_type: type of beam support. expected value: 'cantilever', 'simply_supported'

def beam_deflection(F = None, x = None, material = None, xsection = None, a = None, L = None, support_type = None):
    F = float(F)
    x = float(x)
    a = float(a)
    L = float(L)
    if support_type == 'cantilever':
        if 0.0 <= x < a:
            return (-F * x ** 2 * (3 * a - x)) / (6 * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * a ** 2 * (3 * x - a)) / (6 * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a)
    elif support_type == 'simply_supported':
        b = (L - a)
        if 0.0 <= x < a:
            return (-F * b * x * (L ** 2 - x ** 2 - (L - a) **2)) / (6 * L * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * b * ( ((L / b) * (x - a) ** 3) + ((L ** 2 - b ** 2) * x) - (x**3) ) ) / (6 * L * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)
    
    
def calc_I(xsection = None):
    if xsection['type'] == 'rectangular':
        return (xsection['b'] * xsection['h'] ** 3) / 12
    elif xsection['type'] == 'circle':
        return (np.pi * xsection['r'] ** 4) / 4
    else:
        raise Exception(error_msg_xsection)
    
# print( beam_deflection(F = 113.2, x = 2.3, material = 'aluminum', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'wood', xsection = {'type': 'circle', 'r': 3.2}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'steel', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='simply_supported') )

def beam_shear_force(F = None, x = None, a = None, L = None, support_type = None):
    if support_type == 'cantilever':
        if 0.0 <= x < L:
            return F
        else:
            raise Exception(error_msg_a)
    elif support_type == 'simply_supported':
        b = L - a
        if 0.0 <= x < a:
            return (F * b) / L
        elif a <= x <= L:
            return (-F * a) / L
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)
    
# print( beam_shear_force(F = 113.2, x = 2.3, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 7.2, a = 7.1, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 1.3, a = 7.6, L = 10.0, support_type='simply_supported') )
# print( beam_shear_force(F = 113.2, x = 8.1, a = 7.6, L = 10.0, support_type='simply_supported') )
    
def beam_bending_moment(F = None, x = None, a = None, L = None, support_type = None):
    if support_type == 'cantilever':
        return -F * (L - x)
    elif support_type == 'simply_supported':
        b = L - a
        M_max = (F * a * b) / L
        if 0.0 <= x < a:
            return (x / a) * M_max
        elif a <= x <= L:
            return M_max * ( (-(x - a) / b) + 1)
        else:
            raise Exception(error_msg_a)
    else:
        raise Exception(error_msg_support_type)

# print( beam_bending_moment(F = 113.2, x = 0.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 5.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 10.0, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_bending_moment(F = 113.2, x = 0.0, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 2.0, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 4.3, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 5.7, a = 4.3, L = 10.0, support_type='simply_supported') )
# print( beam_bending_moment(F = 113.2, x = 10.0, a = 4.3, L = 10.0, support_type='simply_supported') )

def calc_A(xsection = None):
    if xsection['type'] == 'rectangular':
        return xsection['b'] * xsection['h']
    elif xsection['type'] == 'circle':
        return np.pi * xsection['r'] ** 2
    else:
        raise Exception(error_msg_xsection)
    
def beam_shear_stress(F = None, x = None, xsection = None, a = None, L = None, support_type = None):
    return beam_shear_force(F, x, a, L, support_type) / calc_A(xsection)

def calc_c(xsection = None):
    if xsection['type'] == 'rectangular':
        return 0.5 * xsection['h']
    elif xsection['type'] == 'circle':
        return xsection['r']
    else:
        raise Exception(error_msg_xsection)
    
def beam_bending_stress(F = None, x = None, xsection = None, a = None, L = None, support_type = None):
    F = float(F)
    x = float(x)
    a = float(a)
    L = float(L)
    return beam_bending_moment(F, x, a, L, support_type) * calc_c(xsection) / calc_I(xsection)


#######################################################################
# Application
#######################################################################

app = dash.Dash(__name__)
app.layout = html.Div([
    #
    # Header
    #
    html.H1(
        children="Beam Bending Visualization",
        style={
            'textAlign': 'center',
        }),
    #
    # Inputs
    #
    html.H2("Input Parameters"),
    html.Div([
        html.Div([
            html.Label('Material'),
            dcc.RadioItems(
                id='material-type',
                options=[
                    {'label': 'Aluminum', 'value': 'aluminum'},
                    {'label': 'Wood', 'value': 'wood'},
                    {'label': 'Titanium', 'value': 'titanium'},
                    {'label': 'Steel', 'value': 'steel'}
                ],
                labelStyle={'display': 'block'},
                value='aluminum'
            ),
        ], style={'width': '10%'}),
        html.Div([
            html.Label('Support Type'),
            dcc.RadioItems(
                id='support-type',
                options=[
                    {'label': 'Simply Supported', 'value': 'simply_supported'},
                    {'label': 'Cantilever', 'value': 'cantilever'},
                ],
                labelStyle={'display': 'block'},
                value='simply_supported'
            ),
        ], style={'width': '10%'}),
        html.Div([
            html.Label('Beam Length'),
            dcc.Input(id="beam-length", type="number", step=0.1, value=10.0),
            html.Label('Beam Cross Section'),
            dcc.Dropdown(
                id='xsection',
                options=[
                    {'label': 'Rectangular', 'value': 'rectangular'},
                    {'label': 'Circle', 'value': 'circle'}
                ],
                value='rectangular'
            ),
            html.Div(id='xsection-container', children=
                [
                dcc.Input(id="b", type="number", step=0.1, value=5.0),
                dcc.Input(id="h", type="number", step=0.1, value=10.0),
                dcc.Input(id="r", type="number", value=5.0)
                ]),
        ], style={'paddingRight': 40, 'width': '10%'}),
        html.Div([
            html.Label('Force Magnitude'),
            dcc.Slider(
                id='force-mag',
                min=1,
                max=100,
                marks={
                    1: {'label': '1N', 'style': {'color': '#77b0b1'}},
                    100: {'label': '100N', 'style': {'color': '#f50'}}},
                tooltip={"placement": "bottom", "always_visible": True},
                value=50,
            ),
            html.Br(),
            html.Label('Force Location'),
            dcc.Slider(
                id='force-location', 
                min=1,
                step=0.1,
                max=10,
                marks={
                    1: {'label': '1m', 'style': {'color': '#77b0b1'}},
                    10: {'label': '10m', 'style': {'color': '#f50'}}},
                tooltip={"placement": "bottom", "always_visible": True},
                value=10,
            )
        ], style={'width': '20%'})
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    #
    # Visualization
    #
    html.H2("Visualization"),
    html.Div([
        html.Div([
            dcc.Graph(
                id='graph'
            )
        ], style={'flex': 1})
    ])
])

@app.callback(
    Output('force-location', 'max'),
    Output('force-location', 'value'),
    Output('force-location', 'marks'),
    Input('beam-length', 'value')
)
def update_force_location_range(bl):
    end_label = str(float(bl) - 0.1) + 'm'
    marks={
        1: {'label': '1m', 'style': {'color': '#77b0b1'}},
        float(bl) - 0.1: {'label': end_label, 'style': {'color': '#f50'}}}
    loc = float(bl) - 0.1
    max = float(bl) - 0.1
    #print(max, loc, marks)
    return [ max, loc, marks ]

@app.callback(
    Output('xsection-container', 'children'),
    Input('xsection', 'value')
)
def update_cross_section_container(value):
    print('You have selected "{}"'.format(value))
    
    rectangular = {'display': 'none'}
    circle = {'display': 'none'}
    imageURL = ''
    
    if value == 'rectangular':
        rectangular = {'display': 'block'}
        circle = {'display': 'none'}
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/rect_xsection.png'
    elif value == 'circle':    
        rectangular = {'display': 'none'}
        circle = {'display': 'block'}
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/circle_xsection.png'
    
    return [
            html.Br(style=rectangular),
            html.Img(src=imageURL),
            html.Label('b', style=rectangular),
            dcc.Input(id="b", type="number", step=0.1, value=5.0, style=rectangular),
            html.Label('h', style=rectangular),
            dcc.Input(id="h", type="number", step=0.1, value=10.0, style=rectangular),
            html.Br(style=circle),
            html.Label('Radius', style=circle),
            dcc.Input(id="r", type="number", value=5.0, style=circle),
        ]

@app.callback(
    Output('graph', 'figure'),
    Input('material-type', 'value'),
    Input('support-type', 'value'),
    Input('beam-length', 'value'),
    Input('xsection', 'value'),
    Input('force-location', 'value'),
    Input('force-mag', 'value'),
    Input('b', 'value'),
    Input('h', 'value'),
    Input('r', 'value')
)
def update_graph(mt, st, bl, xs, fl, fm, b, h, r):
    print('------')
    print('You have selected Material Type : "{}"'.format(mt))
    print('You have selected Support Type : "{}"'.format(st))
    print('You have selected Beam Length : "{}"'.format(bl))
    print('You have selected XSection : "{}"'.format(xs))
    print('You have selected Force Location : "{}"'.format(fl))
    print('You have selected Force Mag : "{}"'.format(fm))
    print('You have selected b : "{}"'.format(b))
    print('You have selected h : "{}"'.format(h))
    print('You have selected r : "{}"'.format(r))
    print('------')
    
    xsection = {}
    if xs == 'rectangular':
        xsection['type'] = 'rectangular'
        xsection['b'] = float(b)
        xsection['h'] = float(h)
    else:
        xsection['type'] = 'circle'
        xsection['r'] = float(r)

    #print(xsection)

    N = 100
    X = np.linspace(start = 0.0, stop = float(bl), num = N)
    Y = []
    for i in X:
        Y.append(beam_deflection(F = float(fm), x = float(i), material = mt, xsection = xsection, a = float(fl), L = float(bl), support_type = st))
    
    #print(Y)

    span = float(bl)
    layout = go.Layout(
        title = {
            'text': 'Deflection',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor':'top'},
        titlefont = dict(size=15),
        yaxis = dict(
            title='Deflection'
        ),
        xaxis = dict(
            title='Distance (m)',
            range=[-1, span+1]
        ),
        showlegend=False
    )

    line = go.Scatter(
        x = X,
        y = Y,
        mode = 'lines',
        name = 'Deflection',
        line_color = 'orange',
        fill = 'tonexty',
        fillcolor = 'rgba(255, 255, 0, 0.1)'
    )

    axis = go.Scatter(
        x = [0, span],
        y = [0, 0],
        mode = 'lines',
        line_color = 'black'
    )

    fig = go.Figure(data=[line, axis], layout = layout)
    fig.update_layout(transition_duration=50)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
