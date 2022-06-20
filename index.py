from dash import dcc, html, Output, Input
import dash

from app import app
from app import server
from layouts import profit, revenue, ua, dev
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/profit':
         return profit
    elif pathname == '/':
         return profit
    elif pathname == '/apps/revenue':
         return revenue
    elif pathname == '/apps/ua':
         return ua
    elif pathname == '/apps/dev':
         return dev
    else:
        return profit

if __name__ == '__main__':
    app.run_server(debug=False)
