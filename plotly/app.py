import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import glob
import plotly.graph_objs as go

app = dash.Dash(__name__)

data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(data_path[-1])

teams = df_2022['HOST']
year = [x.split('\\')[-1].split('.csv')[0] for x in data_path][:-1]
df = None

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='item-dropdown',
            style={
                "position": "absolute",
                "left": "500px",
                "width": "200px"
            },
            value="Germany"  # Default value for dropdown
        ),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{'label': yr, 'value': yr} for yr in year],
            style={"width": "200px", "left": "100px"},
            value="1934"  # Default value for dropdown
        ),
        
        html.Div(id='output-div'),

        dcc.Graph(id="graph",
                  figure={
                      'layout': {
                          'plot_bgcolor': '#111111',
                          'paper_bgcolor': '#111111'
                          }}),

        html.Div(
            html.P(
                ["This Dashboard contains all the countries which participated in Football Worldcup thoughout the Years.",
                 html.Br(), "The Graph shows the Win and Loss percentage of country participated."],
                style={"text-align": "center"}
            ),  # Set background color and 
            )
    ]# Set background color for the whole layout
    )

@app.callback(
    dash.dependencies.Output('item-dropdown', 'options'),
    dash.dependencies.Output('item-dropdown', 'value'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)
def update_dropdown(value):
    global df
    df = pd.read_csv(f'E:/Workspace/Data Science/Data Science Project/WC2023/archive/{value}.csv')
    options = [{'label': team, 'value': team} for team in df['Team']]
    value = df['Team'].iloc[0]
    return options, value

@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('item-dropdown', 'value')]
)
def update_graph(selected_team):
    global df
    filtered_df = df[df['Team'] == selected_team]
    filtered_df['WinPercentage'] = (filtered_df['Win'] / filtered_df['Games Played']) * 100
    filtered_df['LossPercentage'] = (filtered_df['Loss'] / filtered_df['Games Played']) * 100
    filtered_df['DrawPercentage'] = (filtered_df['Draw'] / filtered_df['Games Played']) * 100
    win_percentage = filtered_df['WinPercentage'].iloc[0]
    loss_percentage = filtered_df['LossPercentage'].iloc[0]
    draw_percentage = filtered_df['DrawPercentage'].iloc[0]
    fig = go.Figure(data=[go.Pie(labels=['Win', 'Loss', 'Draw'], values=[win_percentage, loss_percentage, draw_percentage])])
    fig.update_layout(title={'text': f'Win-Loss Percentage for {selected_team}', 'x': 0.5})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
