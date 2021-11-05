import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from dash_table.Format import Format, Group


# import pandas as pd
# import requests
# from utils import countries_update_df
from datetime import datetime
import utils

# df = utils.countries_update_df()
sync_data = utils.sync_status_df()
app = dash.Dash(__name__)

countries = ['UK', 'Ireland', 'Spain', 'Netherlands']
# 
# # To know the minimum and the maximum values of date for slicer
# df_stat_metadata = pd.read_json('country_updates.ena.json')
# min_date, max_date = min_max_date(df_stat_metadata)
# 
# # create the dictionary of slider
# marks_data = slicer(min_date, max_date)
# min_max_date_value = [min_date, max_date]


# app.layout = dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     data=df.to_dict('records'),
# )

########
table_header_style = {
    "backgroundColor": "rgb(194,197,204)",
    "color": "white",
    "textAlign": "center",
}

sync_columns = [
    dict(id='Resource', name='Resource', type='text'),
    dict(id='Sequences', name='Sequences', type='numeric', format=Format().group(True)),
    dict(id='Raw Reads', name='Raw Reads', type='numeric', format=Format().group(True)),
]

app.layout = html.Div(
    className="",
    children=[
        html.Div(
            className="header-title",
            children=[
                html.H2(
                    id="title",
                    children="COVID-19 Tracking",
                ),
                html.Div(
                    id="learn_more",
                    children=[
                        html.Img(className="logo", src=app.get_asset_url("logo.png"))
                    ],
                ),
            ],
        ),
        html.Div(
            id="grid",
            children=[
                html.Div(
                className="container",
                children=[
                    html.Div(
                        className="row",
                        style={},
                        children=[
                            html.Div(
                                className="two columns",
                                children= [
                                    html.Button('Refresh Data', id='refresh-data'),
                                    html.Div(id="last-update")
                                ],
                            ),
                            html.Div(
                                className="ten columns",
                                children=[
                                    dash_table.DataTable(
                                        id='table',
                                        columns=sync_columns,
                                        data=sync_data.to_dict('records'),
                                        style_header=table_header_style,
                                        style_cell={'fontSize':18, 'font-family':'sans-serif'}
                                    )
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        id="controls",
                        className="row div-row div-card",
                        children=[
                            html.Div(
                                id="dataset-picker",
                                children=[
                                    html.Div(
                                        className="six columns",
                                        children=[
                                            html.H6(children="Dataset"),
                                            dcc.Dropdown(
                                                id="d_country",
                                                options=[
                                                    {
                                                        "label": countries[i],
                                                        "value": countries[i],
                                                    }
                                                    for i in range(len(countries))
                                                ],
                                                value="UK",
                                            ),
                                            html.Div(id="output-container"),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            )],
        ),
    ],
)
@app.callback(
    Output('last-update','children'),
    [Input('refresh-data','n_clicks')])
def refresh_data(value):
    global df
    df = utils.sync_status_df()
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.callback(Output("output-container", "children"), [Input("d_country", "value")])
def _update_legend_country(country):
    return 'You have selected "{}"'.format(country)



if __name__ == '__main__':
    app.run_server(debug=True)
