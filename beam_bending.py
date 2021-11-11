import dash
import numpy as np
import plotly.graph_objects as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Young's modulus constant in Pascal
E = {
    'aluminum': 68.0 * 10 ** 9,
    'wood': 10.0 * 10 ** 9,
    'titanium': 116.0 * 10 ** 9,
    'steel': 200.0 * 10 ** 9, }

error_msg_a = 'Is a between 0 and L? a: '
error_msg_support_type = 'Invalid support_type'
error_msg_xsection = 'Invalid xsection'


# F: force magnitude in newtons. this is a float.
# x: inspection location, beam deflection at this location, in meters. this is a float.
# material: will affect E (Young's modulus). expected value: 'aluminum', 'wood', 'titanium', 'steel'
# xsection: beam cross section geometry in meters. will affect I. expected value: {'type': 'rectangular', 'b': float, 'h': float}, {'type': 'circle', 'r': float}
# a: force location from left end of beam in meters. this is a float.
# L: total length of beam in meters. this is a float.
# support_type: type of beam support. expected value: 'cantilever', 'simply_supported'

def beam_deflection(F=None, x=None, material=None, xsection=None, a=None, L=None, support_type=None):
    x = max(0, min(x, L))

    if support_type == 'cantilever':
        if 0.0 <= x < a:
            return (-F * x ** 2 * (3 * a - x)) / (6 * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * a ** 2 * (3 * x - a)) / (6 * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a + str(a))
    elif support_type == 'simply_supported':
        b = (L - a)
        if b == 0:
            return 0.0

        if 0.0 <= x < a:
            return (-F * b * x * (L ** 2 - x ** 2 - (L - a) ** 2)) / (6 * L * E[material] * calc_I(xsection))
        elif a <= x <= L:
            return (-F * b * (((L / b) * (x - a) ** 3) + ((L ** 2 - b ** 2) * x) - (x ** 3))) / (
                    6 * L * E[material] * calc_I(xsection))
        else:
            raise Exception(error_msg_a + f'a: {a} L: {L} x: {x}')
    else:
        raise Exception(error_msg_support_type)


def calc_I(xsection=None):
    if xsection['type'] == 'rectangular':
        return (xsection['b'] * xsection['h'] ** 3) / 12
    elif xsection['type'] == 'circle':
        return (np.pi * xsection['r'] ** 4) / 4
    else:
        raise Exception(error_msg_xsection)


# print( beam_deflection(F = 113.2, x = 2.3, material = 'aluminum', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'wood', xsection = {'type': 'circle', 'r': 3.2}, a = 5.0, L = 10.0, support_type='cantilever') )
# print( beam_deflection(F = 113.2, x = 2.3, material = 'steel', xsection = {'type': 'rectangular', 'b': 3.2, 'h': 5.3}, a = 5.0, L = 10.0, support_type='simply_supported') )

def beam_shear_force(F=None, x=None, a=None, L=None, support_type=None):
    x = max(0, min(x, L))

    if support_type == 'cantilever':
        if 0.0 <= x <= L:
            return F
        else:
            raise Exception(error_msg_a + str(a) + str(L))
    elif support_type == 'simply_supported':
        b = L - a
        if 0.0 <= x <= a:
            return (F * b) / L
        elif a < x <= L:
            return (-F * a) / L
        else:
            raise Exception(error_msg_a + str(a))
    else:
        raise Exception(error_msg_support_type)


# print( beam_shear_force(F = 113.2, x = 2.3, a = 3.2, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 7.2, a = 7.1, L = 10.0, support_type='cantilever') )
# print( beam_shear_force(F = 113.2, x = 1.3, a = 7.6, L = 10.0, support_type='simply_supported') )
# print( beam_shear_force(F = 113.2, x = 8.1, a = 7.6, L = 10.0, support_type='simply_supported') )

def beam_bending_moment(F=None, x=None, a=None, L=None, support_type=None):
    x = max(0, min(x, L))

    if support_type == 'cantilever':
        return -F * (L - x)
    elif support_type == 'simply_supported':
        b = L - a
        M_max = (F * a * b) / L
        if a == 0.0:
            return 0.0
        elif 0.0 <= x <= a:
            return (x / a) * M_max
        elif a < x <= L:
            return M_max * ((-(x - a) / b) + 1)
        else:
            raise Exception(error_msg_a + str(a))
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

def calc_A(xsection=None):
    if xsection['type'] == 'rectangular':
        return xsection['b'] * xsection['h']
    elif xsection['type'] == 'circle':
        return np.pi * xsection['r'] ** 2
    else:
        raise Exception(error_msg_xsection)


def beam_shear_stress(F=None, x=None, xsection=None, a=None, L=None, support_type=None):
    return beam_shear_force(F, x, a, L, support_type) / calc_A(xsection)


def calc_c(xsection=None):
    if xsection['type'] == 'rectangular':
        return 0.5 * xsection['h']
    elif xsection['type'] == 'circle':
        return xsection['r']
    else:
        raise Exception(error_msg_xsection)


def beam_bending_stress(F=None, x=None, xsection=None, a=None, L=None, support_type=None):
    return beam_bending_moment(F, x, a, L, support_type) * calc_c(xsection) / calc_I(xsection)


def von_mises_stress(F=None, x=None, xsection=None, a=None, L=None, support_type=None):
    return (beam_bending_stress(F, x, xsection, a, L, support_type) ** 2 + 3 * beam_shear_stress(F, x, xsection, a, L,
                                                                                                 support_type) ** 2) ** 0.5


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
            html.Label('Beam Length (m)'),
            dcc.Input(id="beam-length", type="text", step=0.001, value=10.0, style={'width': '100%'}),
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
                dcc.Input(id="b", type="text", step=0.1, value=0.1),
                dcc.Input(id="h", type="text", step=0.1, value=0.1),
                dcc.Input(id="r", type="text", value=0.1)
            ]),
        ], style={'paddingRight': 40, 'width': '20%'}),
        html.Div([
            html.Label('Force Magnitude (N)'),
            dcc.Input(id="force-mag", type="text", step=0.001, value=500.0, style={'width': '100%'}),
            html.Br(),
            html.Label('Force Location (x)'),
            dcc.Slider(
                id='force-location',
                min=0,
                step=0.001,
                max=10,
                marks={
                    0: {'label': '0m', 'style': {'color': '#77b0b1'}}},
                tooltip={"placement": "bottom", "always_visible": True},
                value=10,
            )
        ], style={'paddingRight': 40, 'width': '20%'}),
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
            html.Div(id='support-type-image', children=[]),
        ], style={'width': '50%'}),
    ], style={'display': 'flex', 'flex-direction': 'row'}),
    #
    # Visualization
    #
    html.H2("Visualization"),
    html.Label('Coloring'),
    dcc.RadioItems(
        id='colormap-selection',
        options=[
            {'label': 'Deflection', 'value': 'deflection'},
            {'label': 'Von Mises', 'value': 'von_mises'},
        ],
        labelStyle={'display': 'block'},
        value='deflection'
    ),
    html.Div([
        html.Div([
            dcc.Graph(
                id='deflection_3d'
            )
        ], style={'flex': 1}),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='deflection_graph'
            )
        ], style={'flex': 1})
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='shear_stress_graph'
            )
        ], style={'flex': 1})
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='bending_stress_graph'
            )
        ], style={'flex': 1})
    ]),
    html.Div([
        html.Div([
            dcc.Graph(
                id='von_mises_graph'
            )
        ], style={'flex': 1})
    ]),
])


@app.callback(
    Output('force-location', 'max'),
    Output('force-location', 'value'),
    # Output('force-location', 'marks'),
    Input('beam-length', 'value')
)
def update_force_location_range(bl):
    # marks={
    #     0: {'label': '0m', 'style': {'color': '#77b0b1'}},
    #     str(bl): {'label': f'{bl}m', 'style': {'color': '#f50'}}}
    loc = float(bl) / 2
    max = float(bl)
    # print(max, loc, marks)
    return [max, loc]


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
        rectangular = {'display': 'block', 'width': '100%'}
        circle = {'display': 'none', 'width': '100%'}
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/rect_xsection.png'
    elif value == 'circle':
        rectangular = {'display': 'none', 'width': '100%'}
        circle = {'display': 'block', 'width': '100%'}
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/circle_xsection.png'

    return [
        html.Br(style=rectangular),
        html.Img(src=imageURL, style={'objectFit': 'contain', 'width': '100%'}),
        html.Label('b (m)', style=rectangular),
        dcc.Input(id="b", type="text", step=0.001, value=0.1, style=rectangular),
        html.Label('h (m)', style=rectangular),
        dcc.Input(id="h", type="text", step=0.001, value=0.1, style=rectangular),
        html.Br(style=circle),
        html.Label('Radius (m)', style=circle),
        dcc.Input(id="r", type="text", step=0.001, value=0.1, style=circle),
    ]


@app.callback(
    Output('support-type-image', 'children'),
    Input('support-type', 'value')
)
def update_cross_section_container(value):
    imageURL = ''
    if value == 'cantilever':
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/cantilever.png'
    elif value == 'simply_supported':
        imageURL = 'https://raw.githubusercontent.com/bokilenator/CS-519-Beam-Bending-Visualization/main/simply_supported.png'

    return [html.Img(src=imageURL), ]


@app.callback(
    Output('deflection_graph', 'figure'),
    Output('shear_stress_graph', 'figure'),
    Output('bending_stress_graph', 'figure'),
    Output('von_mises_graph', 'figure'),
    Output('deflection_3d', 'figure'),
    Input('material-type', 'value'),
    Input('support-type', 'value'),
    Input('beam-length', 'value'),
    Input('xsection', 'value'),
    Input('force-location', 'value'),
    Input('force-mag', 'value'),
    Input('b', 'value'),
    Input('h', 'value'),
    Input('r', 'value'),
    Input('colormap-selection', 'value'),
)
def update_graph(mt, st, bl, xs, fl, fm, b, h, r, cm):
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
    print('You have selected colormap : "{}"'.format(cm))
    print('------')

    xsection = {}
    if xs == 'rectangular':
        xsection['type'] = 'rectangular'
        xsection['b'] = float(b)
        xsection['h'] = float(h)
    else:
        xsection['type'] = 'circle'
        xsection['r'] = float(r)

    # print(xsection)

    # still need to figure out how to turn into rectangle, right now just pixel size for cylinder
    bar_width = 15
    step = 0.01
    X = np.arange(start=0.0, stop=float(bl) + step, step=step)
    # X = np.linspace(start = 0.0, stop = float(bl), num = N)
    X = np.sort(np.append(X, float(fl)))  ## make sure crictical point is in the array
    Y = []
    shear_stress = []
    bending_stress = []
    vonmises_stress = []
    for i in X:
        Y.append(beam_deflection(F=float(fm), x=float(i), material=mt, xsection=xsection, a=float(fl), L=float(bl),
                                 support_type=st))
        shear_stress.append(
            beam_shear_stress(F=float(fm), x=float(i), xsection=xsection, a=float(fl), L=float(bl), support_type=st))
        bending_stress.append(
            beam_bending_stress(F=float(fm), x=float(i), xsection=xsection, a=float(fl), L=float(bl), support_type=st))
        vonmises_stress.append(
            von_mises_stress(F=float(fm), x=float(i), xsection=xsection, a=float(fl), L=float(bl), support_type=st))

    # print(Y)

    span = float(bl)
    layout_deflection = go.Layout(
        title={
            'text': 'Deflection',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        yaxis=dict(
            title='Deflection (m)',
            showexponent='all',
            exponentformat='e'
        ),
        xaxis=dict(
            title='Distance (m)',
            range=[0, span]
        ),
        showlegend=False
    )
    layout_deflection_3d = go.Layout(
        title={
            'text': '3D Deflection',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        scene=dict(
            xaxis=dict(
                title='Distance (m)',
                range=[-1, span]
            ),
            yaxis=dict(
                title='Deflection (m)',
                showexponent='all',
                exponentformat='e',
                range=[-1 * span, span]
            )
        ),
        showlegend=False
    )

    layout_shear_stress = go.Layout(
        title={
            'text': 'Shear Stress',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        yaxis=dict(
            title='Shear Stress (Pascal)',
            showexponent='all',
            exponentformat='e'
        ),
        xaxis=dict(
            title='Distance (m)',
            range=[0, span]
        ),
        showlegend=False
    )

    layout_bending_stress = go.Layout(
        title={
            'text': 'Bending Stress',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        yaxis=dict(
            title='Bending Stress (Pascal)',
            showexponent='all',
            exponentformat='e'
        ),
        xaxis=dict(
            title='Distance (m)',
            range=[0, span]
        ),
        showlegend=False
    )

    layout_vonmises_stress = go.Layout(
        title={
            'text': 'Von Mises Stress',
            'y': 0.85,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        titlefont=dict(size=15),
        yaxis=dict(
            title='Von Mises Stress (Pascal)',
            showexponent='all',
            exponentformat='e'
        ),
        xaxis=dict(
            title='Distance (m)',
            range=[0, span]
        ),
        showlegend=False
    )

    line_deflection = go.Scatter(
        x=X,
        y=Y,
        mode='lines',
        name='Deflection',
        line_color='orange',
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.1)'
    )

    line_shear_stress = go.Scatter(
        x=X,
        y=shear_stress,
        mode='lines',
        name='Shear Stress',
        line_color='orange',
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.1)'
    )

    line_bending_stress = go.Scatter(
        x=X,
        y=bending_stress,
        mode='lines',
        name='Bending Stress',
        line_color='orange',
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.1)'
    )

    line_vonmises_stress = go.Scatter(
        x=X,
        y=vonmises_stress,
        mode='lines',
        name='Von Mises Stress',
        line_color='orange',
        fill='tonexty',
        fillcolor='rgba(255, 255, 0, 0.1)'
    )

    color = None
    title = None
    if cm == 'deflection':
        color = Y
        title = 'Deflection (m)'
    elif cm == 'von_mises':
        color = vonmises_stress
        title = 'Stress (Pa)'
        
    line_3d_deflection = go.Scatter3d(
        x=X, z=Y, y=[0] * len(X),
        marker=dict(
            size=bar_width,
            color=color,
            colorscale='redor',
            colorbar=dict(
                title=title,
                exponentformat='e',
            ),
            symbol="square" if xs == "rectangular" else "circle"
        ),
        line=dict(
            color='darkblue',
            width=10
        ),
    )

    axis = go.Scatter(
        x=[0, span],
        y=[0, 0],
        mode='lines',
        line_color='black'
    )

    deflection = go.Figure(data=[line_deflection, axis], layout=layout_deflection)
    shear = go.Figure(data=[line_shear_stress], layout=layout_shear_stress)
    bending = go.Figure(data=[line_bending_stress], layout=layout_bending_stress)
    vonmises = go.Figure(data=[line_vonmises_stress], layout=layout_vonmises_stress)
    deflection_3d = go.Figure(data=line_3d_deflection, layout=layout_deflection_3d)

    deflection.update_layout(transition_duration=50)

    return deflection, shear, bending, vonmises, deflection_3d


if __name__ == '__main__':
    app.run_server(debug=True)
