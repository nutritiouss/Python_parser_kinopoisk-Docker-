import dash
import dash_core_components as dcc
import dash_html_components as html
from helper import concat_dataframes

# the group  and sort data
_df = concat_dataframes().groupby('genre').count().\
                        reset_index()[['genre','film_name']].\
                        sort_values(by='film_name',ascending=False)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='ТОП-250 сериалов с кинопоиска по жанрам'),

    html.Div(children='''
        Dash: 
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': _df['genre'].to_list(), 'y': _df['film_name'].to_list(), 'type': 'bar', 'name': 'TOP-250'},

            ],
            'layout': {
                'title': 'Распределение жанров'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
