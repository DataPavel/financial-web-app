import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

import dash
from dash import dcc, html, Output, Input
from app import app

df = pd.read_csv('data//GL.csv')
banks = pd.read_csv('data//Banks.csv')
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

dd1_2 = {}
for d1 in dd1:
    d2 = df.query('Company == @d1')['Studio'].unique()
    dd1_2[d1] = d2

### Dropdown by Project

dd3 = df.Project.unique()
dd3_all_2 = [
    {'label': k, 'value': k} for k in sorted(dd3)
]
dd3_all_1 = [{'label': '(Select All)', 'value': 'All'}]

project = dd3_all_1 + dd3_all_2

dd2_3 = {}
for d2 in dd2:
    d3 = df.query('Studio == @d2')['Project'].unique()
    dd2_3[d2] = d3

### Modification of dataset

month_to_str = {1: "Jan'21", 2: "Feb'21", 3: "Mar'21", 4: "Apr'21", 5: "May'21",
           6: "Jun'21", 7: "Jul'21", 8: "Aug'21", 9: "Sep'21", 10: "Oct'21",
           11: "Nov'21", 12: "Dec'21"}

df['Date'] = pd.to_datetime(df['Date'])
df['month'] = pd.DatetimeIndex(df['Date']).month
df['mon_str'] = df['month'].map(month_to_str)
df['amount_abs'] = df['Amount_USD'].abs()
banks['Date'] = pd.to_datetime(banks['Date'])
banks['month'] = pd.DatetimeIndex(banks['Date']).month
banks['mon_str'] = banks['month'].map(month_to_str)


############################# Modification of studio filter ####################
@app.callback(
    Output('studio', 'options'),
    [Input('legal', 'value')]
)

def studio_options(legal_value):
    isselect_all = 'Start' #Initialize isselect_all
    #Rembember that the dropdown value is a list !
    for i in legal_value:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        else:
            pass
    #Create options for individual selections
    if isselect_all == 'N':
        options_0 = []
        for i in legal_value:
            options_0.append(dd1_2[i])
        options_1 = [] # Extract string of string
        for i1 in options_0:
            for i2 in i1:
                options_1.append(i2)
        options_list = [] # Get unique values from the string
        for i in options_1:
            if i not in options_list:
                options_list.append(i)
            else:
                pass
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(options_list)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1
    #Create options for select all or none
    else:
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(dd2)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final

############################# Modification of project filter ###################

@app.callback(
    Output('project', 'options'),
    [Input('studio', 'value')]
)

def project_options(studio_value):
    isselect_all = 'Start' #Initialize isselect_all
    #Rembember that the dropdown value is a list !
    for i in studio_value:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        else:
            pass
    #Create options for individual selections
    if isselect_all == 'N':
        options_0 = []
        for i in studio_value:
            options_0.append(dd2_3[i])
        options_1 = [] # Extract string of string
        for i1 in options_0:
            for i2 in i1:
                options_1.append(i2)
        options_list = [] # Get unique values from the string
        for i in options_1:
            if i not in options_list:
                options_list.append(i)
            else:
                pass
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(options_list)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1
    #Create options for select all or none
    else:
        options_final_1 = [
            {'label' : k, 'value' : k} for k in sorted(dd3)]
        options_final_0 = [{'label' : '(Select All)', 'value' : 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final

################################Metric selection #############################
@app.callback(Output("url", "pathname"), Input("page_dd", "value"))
def update_url_on_dropdown_change(dropdown_value):
    return dropdown_value

################################################################################
################################## Profit page #################################
################################################################################
############################ Revenue by month bar chart ########################

@app.callback(
    Output('profit_bar_month', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio

    dff = df_project[(df_project['month']>= month_chosen[0]) & (df_project['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str'])['Amount_USD'].sum().reset_index()
    dff1['Color'] = np.where(dff1['Amount_USD']<0, '#F43B76', '#3D60A2')

    barchart = go.Figure()
    barchart.add_trace(
                go.Bar(
                    x=dff1['mon_str'],
                    y=dff1['Amount_USD'],
                    marker_color=dff1['Color'],
                    text = dff1['Amount_USD']
                    )
                        )
    barchart.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1.5

    )
    barchart.update_xaxes(title = None,
                            tickfont=dict(size=8))
    barchart.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    barchart.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Profit by Month, USD",
                           'x':0.5
                                 },
                    plot_bgcolor='#F3FEFE'
                    )

    return (barchart)

############################ Cash balances line chart ########################

@app.callback(
    Output('cash', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value')
    ]
)

def update_graph(month_chosen, legaldd):

    isselect_all_dd1 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = banks.loc[banks['Company'].isin(legaldd), :].copy()
    else:
        df_legal = banks.copy()


    dff = df_legal[(df_legal['month']>= month_chosen[0]) & (df_legal['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str'])['Amount_USD'].sum().reset_index()

    linechart = px.area(dff1, x = 'mon_str', y = 'Amount_USD',
            text = 'Amount_USD',
            markers = True,
            color_discrete_sequence=['#36CE53'],
            template = 'simple_white'
                    )
    linechart.update_traces(
                            texttemplate='%{text:.2s}',
                            textposition = 'top center',
                            textfont_size = 10,
                            )
    linechart.update_xaxes(title = None,
                            tickfont=dict(size=8))
    linechart.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    linechart.update_layout(
                            # width = 600, height = 270,
                            yaxis_range=[0,1700000],
                            xaxis_range= [-0.5, dff1['month'].max() - 0.5],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "Cash Balances",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            paper_bgcolor= '#ECF0F1'
                            )


    return (linechart)


############################ Cumulative revenue line chart ########################

@app.callback(
    Output('profit_cumulative', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio

    dff = df_project[(df_project['month']>= month_chosen[0]) & (df_project['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str'])['Amount_USD'].sum().reset_index()
    dff1['RT'] = dff1['Amount_USD'].cumsum()
    dff1['Color'] = np.where(dff1['RT']<0, '#F43B76', '#36CE53')
    cumline = px.area(dff1, x = 'mon_str', y = 'RT',
            text = 'RT',
            markers = True,
            color_discrete_sequence= dff1['Color'],
            template = 'simple_white'
                    )
    cumline.update_traces(
                            texttemplate='%{text:.2s}',
                            textposition = 'top center',
                            textfont_size = 10,
                            marker_color=dff1['Color'],
                            )
    cumline.update_xaxes(title = None,
                            tickfont=dict(size=8))
    cumline.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    cumline.update_layout(
                            # width = 600, height = 270,
                            # yaxis_range=[0,1700000],
                            xaxis_range= [-0.5, dff1['month'].max() - 0.5],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "Cumulative profit, USD",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            paper_bgcolor= '#ECF0F1'
                            )


    return (cumline)

############################ Profit by project ########################

@app.callback(
    Output('project_bar', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio

    dff = df_project[(df_project['month']>= month_chosen[0]) & (df_project['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Project'])['Amount_USD'].sum().reset_index()
    dff1['Color'] = np.where(dff1['Amount_USD']<0, '#F43B76', '#3D60A2')

    barproject = go.Figure()
    barproject.add_trace(
                go.Bar(
                    x=dff1['Project'],
                    y=dff1['Amount_USD'],
                    marker_color=dff1['Color'],
                    text = dff1['Amount_USD']
                    )
                        )
    barproject.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1.5

    )
    barproject.update_xaxes(title = None,
                            tickfont=dict(size=8))
    barproject.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    barproject.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Profit by Project, USD",
                           'x':0.5
                                 },
                    plot_bgcolor='#F3FEFE'
                    )

    return (barproject)
################################################################################
################################# Revenue Page #################################
################################################################################

############################ Revenue by month ##################################

@app.callback(
    Output('revenue_bar_month', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Mobile IAP', 'Revenue from Ads']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str', 'Category'])['Amount_USD'].sum().reset_index()

    barrevenue = px.bar(dff1, x = 'mon_str',
    y = 'Amount_USD',
    color = 'Category',
    text = 'Amount_USD')

    barrevenue.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1

    )
    barrevenue.update_xaxes(title = None,
                            tickfont=dict(size=8))
    barrevenue.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    barrevenue.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Revenue by Month, USD",
                           'x':0.5
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (barrevenue)

############################ Revenue by country ##################################

@app.callback(
    Output('map_revenue', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Mobile IAP', 'Revenue from Ads']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Country_code'])['Amount_USD'].sum().reset_index()


    maprevenue = px.choropleth(dff1, locations = 'Country_code',
                    color="Amount_USD",
                    color_continuous_scale=px.colors.sequential.YlGn)

    maprevenue.update_xaxes(title = None,
                            tickfont=dict(size=8))
    maprevenue.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    maprevenue.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'ggplot2',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Revenue by Country",
                           'x':0.4
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (maprevenue)
############################ Pie revenue by category ##################################

@app.callback(
    Output('distr_IAP_Ads', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Mobile IAP', 'Revenue from Ads']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Category'])['Amount_USD'].sum().reset_index()

    piecatrev = px.pie(dff1, values='Amount_USD',
    names='Category', hole = 0.5
                            )

    piecatrev.update_xaxes(title = None,
                            tickfont=dict(size=8))
    piecatrev.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    piecatrev.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Revenue by Category",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (piecatrev)


############################ Pie Mobile IAP by counterparty ####################

@app.callback(
    Output('IAP_counter', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Mobile IAP']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Counterparty'])['Amount_USD'].sum().reset_index()

    pieIAP = px.pie(dff1, values='Amount_USD', names='Counterparty', hole = 0.5)

    pieIAP.update_xaxes(title = None,
                            tickfont=dict(size=8))
    pieIAP.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    pieIAP.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Mobile IAP by Counterparty",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (pieIAP)
############################ Pie Mobile IAP by counterparty ####################

@app.callback(
    Output('AdsCounter', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Revenue from Ads']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Counterparty'])['Amount_USD'].sum().reset_index()

    pieAds = px.pie(dff1, values='Amount_USD', names='Counterparty', hole = 0.5)

    pieAds.update_xaxes(title = None,
                            tickfont=dict(size=8))
    pieAds.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    pieAds.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Revenue form Ads by Counterparty",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (pieAds)

################################################################################
################################# User acquisition Page ########################
################################################################################

############################ UA by month ##################################

@app.callback(
    Output('ua_bar_month', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['UA']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str',])['amount_abs'].sum().reset_index()


    barua = px.bar(dff1, x = 'mon_str',
    y = 'amount_abs',
    text = 'amount_abs')

    barua.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1

    )
    barua.update_xaxes(title = None,
                            tickfont=dict(size=8))
    barua.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    barua.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "User Acquisition by Month, USD",
                           'x':0.5
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (barua)
############################ UA by country ##################################

@app.callback(
    Output('map_ua', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['UA']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Country_code'])['amount_abs'].sum().reset_index()

    mapua = px.choropleth(dff1, locations = 'Country_code',
                    color="amount_abs",
                    color_continuous_scale=px.colors.sequential.YlGn)

    mapua.update_xaxes(title = None,
                            tickfont=dict(size=8))
    mapua.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    mapua.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'ggplot2',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "User Acquisition by Country",
                           'x':0.4
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (mapua)

############################ Pie UA by counterparty ####################

@app.callback(
    Output('UACounter', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['UA']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Counterparty'])['amount_abs'].sum().reset_index()

    pieUA = px.pie(dff1, values='amount_abs', names='Counterparty', hole = 0.5)

    pieUA.update_xaxes(title = None,
                            tickfont=dict(size=8))
    pieUA.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    pieUA.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "UA by Counterparty",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (pieUA)


################################################################################
################################# Development Page #############################
################################################################################

############################ Development by month ##############################

@app.callback(
    Output('dev_bar_month', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Salaries', 'Licensing']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['month', 'mon_str', 'Category'])['amount_abs'].sum().reset_index()

    bardev = px.bar(dff1, x = 'mon_str',
    y = 'amount_abs',
    color = 'Category',
    text = 'amount_abs')

    bardev.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1

    )
    bardev.update_xaxes(title = None,
                            tickfont=dict(size=8))
    bardev.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    bardev.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Development by Month, USD",
                           'x':0.5
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (bardev)

############################ Development by country ############################

@app.callback(
    Output('map_dev', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Salaries', 'Licensing']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Country_code'])['amount_abs'].sum().reset_index()


    mapdev = px.choropleth(dff1, locations = 'Country_code',
                    color="amount_abs",
                    color_continuous_scale=px.colors.sequential.YlGn)

    mapdev.update_xaxes(title = None,
                            tickfont=dict(size=8))
    mapdev.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    mapdev.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'ggplot2',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Development by Country",
                           'x':0.4
                                 },
                    legend = dict(
                        orientation = 'h',
                        y = -0.15,

                     font=dict(
                        size=12,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (mapdev)

############################ Pie dev by category ##################################

@app.callback(
    Output('distr_dev', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Salaries', 'Licensing']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Category'])['amount_abs'].sum().reset_index()

    piecatdev = px.pie(dff1, values='amount_abs',
    names='Category', hole = 0.5
                            )

    piecatdev.update_xaxes(title = None,
                            tickfont=dict(size=8))
    piecatdev.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    piecatdev.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Development by Category",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (piecatdev)
############################ Pie Development by counterparty ####################

@app.callback(
    Output('dev_counter', 'figure'),
    [Input('range_slider', 'value'),
    Input('legal', 'value'),
    Input('studio', 'value'),
    Input('project', 'value')
    ]
)

def update_graph(month_chosen, legaldd, studiodd, projectdd):

    isselect_all_dd1 = 'start'
    isselect_all_dd2 = 'start'
    isselect_all_dd3 = 'start'

    for i in legaldd:
        if i == 'All':
            isselect_all_dd1 = 'Y'
            break
        elif i != '':
            isselect_all_dd1 = 'N'
        else:
            pass

    if isselect_all_dd1 == 'N':
        df_legal = df.loc[df['Company'].isin(legaldd), :].copy()
    else:
        df_legal = df.copy()

    for i in studiodd:
        if i == 'All':
            isselect_all_dd2 = 'Y'
            break
        elif i != '':
            isselect_all_dd2 = 'N'
        else:
            pass

    if isselect_all_dd2 == 'N':
        df_studio = df_legal.loc[df['Studio'].isin(studiodd), :].copy()
    else:
        df_studio = df_legal.copy()
    del df_legal

    for i in projectdd:
        if i == 'All':
            isselect_all_dd3 = 'Y'
            break
        elif i != '':
            isselect_all_dd3 = 'N'
        else:
            pass

    if isselect_all_dd3 == 'N':
        df_project = df_studio.loc[df['Project'].isin(projectdd), :].copy()
    else:
        df_project = df_studio.copy()
    del df_studio
    dff = df_project.loc[df_project['Category'].isin(['Salaries', 'Licensing']), :]
    dff = dff[(dff['month']>= month_chosen[0]) & (dff['month']<= month_chosen[1])]

    dff1 = dff.groupby(['Counterparty'])['amount_abs'].sum().reset_index()

    # piedevcounter = px.pie(dff1, values='amount_abs', names='Counterparty', hole = 0.5)
    # return (piedevcounter)
    piedevcounter = px.pie(dff1, values='amount_abs', names='Counterparty', hole = 0.5)

    piedevcounter.update_xaxes(title = None,
                            tickfont=dict(size=8))
    piedevcounter.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    piedevcounter.update_layout(
                    # width = 400, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Development by Counterparty",
                           'x':0.5
                                 },
                    legend = dict(
                        # orientation = 'h',
                        # y = -0.15,

                     font=dict(
                        size=10,
                                )),
                    plot_bgcolor='#F3FEFE'
                    )

    return (piedevcounter)
