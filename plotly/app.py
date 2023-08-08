import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd  # Import pandas
import glob

app = dash.Dash(__name__)

data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(data_path[-1])
    
teams = df_2022['HOST']
year = [x.split('\\')[-1].split('.csv')[0] for x in data_path][:-1]




app.layout = html.Div([
    dcc.Dropdown(
        id='item-dropdown',
        options=[{'label': team, 'value': team} for team in teams],  # Corrected
        style={
            "position": "absolute",
            "left": "200px",
            "width": "300px"
        },
        value="Team A"
    ),
    dcc.Dropdown(
        id="category-dropdown",
        options=[{'label': yr, 'value': yr} for yr in year],  # Corrected
        style={"width": "300px"},
        value="1934"
    ),
    html.Div(id='output-div')
])

@app.callback(
    dash.dependencies.Output('item-dropdown', 'options'),
    dash.dependencies.Output('item-dropdown', 'value'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)
def update_dropdown(value):
    df = pd.read_csv(f'E:/Workspace/Data Science/Data Science Project/WC2023/archive/{value}.csv')
    options = [{'label': team, 'value': team} for team in df['Team']]
    value = df['Team'].iloc[0]
    return options, value

@app.callback(
    dash.dependencies.Output('output-div', 'children'),
    [dash.dependencies.Input('item-dropdown', 'value')]
)
def update_output(selected_item):
    return f'You selected: {selected_item}'

if __name__ == '__main__':
    app.run_server(debug=True)
