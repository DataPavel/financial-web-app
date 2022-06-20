import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
from app import app
# Read the data
df = pd.read_csv('data//GL.csv')



# Options for dropdown lists

### Dropdown by legal entity
dd1 = df.Company.unique()
dd1_all_2 = [
    {'label': k, 'value': k} for k in sorted(dd1)
]
dd1_all_1 = [{'label': '(Select All)', 'value': 'All'}]

legal = dd1_all_1 + dd1_all_2


### Dropdown by Studio
dd2 = df.Studio.unique()
dd2_all_2 = [
    {'label': k, 'value': k} for k in sorted(dd2)
]
dd2_all_1 = [{'label': '(Select All)', 'value': 'All'}]

studio = dd2_all_1 + dd2_all_2

### Dropdown by Project

dd3 = df.Project.unique()
dd3_all_2 = [
    {'label': k, 'value': k} for k in sorted(dd3)
]
dd3_all_1 = [{'label': '(Select All)', 'value': 'All'}]

project = dd3_all_1 + dd3_all_2


############################# Dictionaries for dropdown - pages ################
refs = [{'label':'Profit', 'value': '/apps/profit'},
{'label':'Revenue', 'value': '/apps/revenue'},
{'label':'User Acquisition', 'value': '/apps/ua'},
{'label':'Development', 'value': '/apps/dev'}
]
############################## Profit Page #####################################

profit = dbc.Container([dbc.Row([
    dbc.Row([
        dbc.Col(html.H3(children = 'Group Overview',
                        className = 'text-center'),
                        width={"size": 10, "offset": 1}),
        dbc.Col(html.Img(
                        src = app.get_asset_url('cherry.jpg'),
                            height = '50 px',
                            width = 'auto'),
                            width = 1)
    ], style={'height': '80px'}),

    dbc.Row([
        dbc.Col(
            html.H6('Select a metric:'),
            width = {'size': 2, 'offset': 1}),
        dbc.Col(
            html.H6('Select a date range:'),
            width = 2
        ),
        dbc.Col(
            html.H6('Apply filter using dropdown:'),
            width = 2
        )
            ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id = 'page_dd',
                options = refs,
                value = '/apps/profit',
                multi = False,
                placeholder = 'Select metric',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                    width = {'size': 2, 'offset': 1}),
        dbc.Col(
            [dcc.RangeSlider(
                id = 'range_slider',
                marks = {
                        1: "Jan'21",
                        12: "Dec'21",
                            },
                step = 1,
                min = 1,
                max = 12,
                value = [1, 12]
                                )],
                    width = {'size': 2},
                    style = {'margin-top' : '10px'}
                    ),

        dbc.Col([
            dcc.Dropdown(
                id = 'legal',
                options = legal,
                value = [''],
                multi = True,
                placeholder = 'Select legal entity',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'studio',
                options = studio,
                value = [''],
                multi = True,
                placeholder = 'Select studio',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'project',
                options = project,
                value = [''],
                multi = True,
                placeholder = 'Select project',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            )
                ],
                width = 2)
                ], style={'height': '70px'})
    ], className = ['row sticky-top', 'bg-light', 'h-25']),

    dbc.Row([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'cash', style={'height': '40vh'})
        ], width = {'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'profit_bar_month', style={'height': '40vh'})
        ], width = 5)
    ], className = ['bg-light']),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'profit_cumulative', style={'height': '35vh'})
        ], width = {'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'project_bar', style={'height': '35vh'})
        ], width = 5)
    ], className = ['bg-light']),
    ], className = 'h-25')
], fluid = True)

############################## Revenue Page #####################################

revenue = dbc.Container([dbc.Row([
    dbc.Row([
        dbc.Col(html.H3(children = 'Group Overview',
                        className = 'text-center'),
                        width={"size": 10, "offset": 1}),
        dbc.Col(html.Img(
                        src = app.get_asset_url('cherry.jpg'),
                            height = '50 px',
                            width = 'auto'),
                            width = 1)
    ], style={'height': '80px'}),

    dbc.Row([
        dbc.Col(
            html.H6('Select a metric:'),
            width = {'size': 2, 'offset': 1}),
        dbc.Col(
            html.H6('Select a date range:'),
            width = 2
        ),
        dbc.Col(
            html.H6('Apply filter using dropdown:'),
            width = 2
        )
            ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id = 'page_dd',
                options = refs,
                value = '/apps/revenue',
                multi = False,
                placeholder = 'Select metric',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                    width = {'size': 2, 'offset': 1}),
        dbc.Col(
            [dcc.RangeSlider(
                id = 'range_slider',
                marks = {
                        1: "Jan'21",
                        12: "Dec'21",
                            },
                step = 1,
                min = 1,
                max = 12,
                value = [1, 12]
                                )],
                    width = {'size': 2},
                    style = {'margin-top' : '10px'}
                    ),

        dbc.Col([
            dcc.Dropdown(
                id = 'legal',
                options = legal,
                value = [''],
                multi = True,
                placeholder = 'Select legal entity',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'studio',
                options = studio,
                value = [''],
                multi = True,
                placeholder = 'Select studio',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'project',
                options = project,
                value = [''],
                multi = True,
                placeholder = 'Select project',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            )
                ],
                width = 2)
                ], style={'height': '70px'})
    ], className = ['row sticky-top', 'bg-light']),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'revenue_bar_month')
        ], width = {'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'map_revenue')
        ], width = 5)
    ], className = ['bg-light']),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'distr_IAP_Ads')
        ], width = {'size': 3, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'IAP_counter')
        ], width = 4),
        dbc.Col([
            dcc.Graph(id = 'AdsCounter')
        ], width = 3)

    ], className = ['bg-light']),
], fluid = True)

########################## User Acquisition Page ###############################

ua = dbc.Container([dbc.Row([
    dbc.Row([
        dbc.Col(html.H3(children = 'Group Overview',
                        className = 'text-center'),
                        width={"size": 10, "offset": 1}),
        dbc.Col(html.Img(
                        src = app.get_asset_url('cherry.jpg'),
                            height = '50 px',
                            width = 'auto'),
                            width = 1)
    ], style={'height': '80px'}),

    dbc.Row([
        dbc.Col(
            html.H6('Select a metric:'),
            width = {'size': 2, 'offset': 1}),
        dbc.Col(
            html.H6('Select a date range:'),
            width = 2
        ),
        dbc.Col(
            html.H6('Apply filter using dropdown:'),
            width = 2
        )
            ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id = 'page_dd',
                options = refs,
                value = '/apps/ua',
                multi = False,
                placeholder = 'Select metric',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                    width = {'size': 2, 'offset': 1}),
        dbc.Col(
            [dcc.RangeSlider(
                id = 'range_slider',
                marks = {
                        1: "Jan'21",
                        12: "Dec'21",
                            },
                step = 1,
                min = 1,
                max = 12,
                value = [1, 12]
                                )],
                    width = {'size': 2},
                    style = {'margin-top' : '10px'}
                    ),

        dbc.Col([
            dcc.Dropdown(
                id = 'legal',
                options = legal,
                value = [''],
                multi = True,
                placeholder = 'Select legal entity',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'studio',
                options = studio,
                value = [''],
                multi = True,
                placeholder = 'Select studio',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'project',
                options = project,
                value = [''],
                multi = True,
                placeholder = 'Select project',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            )
                ],
                width = 2)
                ], style={'height': '70px'})
    ], className = ['row sticky-top', 'bg-light']),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'ua_bar_month')
        ], width = {'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'map_ua')
        ], width = 5)
    ], className = ['bg-light']),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'UACounter')
        ], width = {'size': 4, 'offset': 5})

    ], className = ['bg-light']),

], fluid = True)
############################## Development Page #####################################

dev = dbc.Container([dbc.Row([
    dbc.Row([
        dbc.Col(html.H3(children = 'Group Overview',
                        className = 'text-center'),
                        width={"size": 10, "offset": 1}),
        dbc.Col(html.Img(
                        src = app.get_asset_url('cherry.jpg'),
                            height = '50 px',
                            width = 'auto'),
                            width = 1)
    ], style={'height': '80px'}),

    dbc.Row([
        dbc.Col(
            html.H6('Select a metric:'),
            width = {'size': 2, 'offset': 1}),
        dbc.Col(
            html.H6('Select a date range:'),
            width = 2
        ),
        dbc.Col(
            html.H6('Apply filter using dropdown:'),
            width = 2
        )
            ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id = 'page_dd',
                options = refs,
                value = '/apps/dev',
                multi = False,
                placeholder = 'Select metric',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                    width = {'size': 2, 'offset': 1}),
        dbc.Col(
            [dcc.RangeSlider(
                id = 'range_slider',
                marks = {
                        1: "Jan'21",
                        12: "Dec'21",
                            },
                step = 1,
                min = 1,
                max = 12,
                value = [1, 12]
                                )],
                    width = {'size': 2},
                    style = {'margin-top' : '10px'}
                    ),

        dbc.Col([
            dcc.Dropdown(
                id = 'legal',
                options = legal,
                value = [''],
                multi = True,
                placeholder = 'Select legal entity',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px',}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'studio',
                options = studio,
                value = [''],
                multi = True,
                placeholder = 'Select studio',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            ),
                ],
                width = 2),

        dbc.Col([
            dcc.Dropdown(
                id = 'project',
                options = project,
                value = [''],
                multi = True,
                placeholder = 'Select project',
                style={'height': '35px', 'width': '170px',
                'font-size': '12px'}
                            )
                ],
                width = 2)
                ], style={'height': '70px'})
    ], className = ['row sticky-top', 'bg-light']),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'dev_bar_month')
        ], width = {'size': 5, 'offset': 1}),
        dbc.Col([
            dcc.Graph(id = 'map_dev')
        ], width = 5)
    ], className = ['bg-light']),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'distr_dev')
        ], width = {'size': 4, 'offset': 2}),
        dbc.Col([
            dcc.Graph(id = 'dev_counter')
        ], width = {'size': 4})
    ], className = ['bg-light'])

], fluid = True)
