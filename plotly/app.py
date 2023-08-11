import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import glob
import plotly.graph_objs as go
import plotly.express as px

app = dash.Dash(__name__)

data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(
    'E:\\Workspace\\Data Science\\Data Science Project\\WC2023\\FIFA - World Cup Summary.csv')

teams = df_2022['HOST']
year = [x.split('\\')[-1].split('.csv')[0] for x in data_path]
df = None

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='item-dropdown',
            style={
                "position": "absolute",
                "left": "500px",
                "width": "300px",
                "border-radius": "1px"
            },
            value="Germany"  # Default value for dropdown
        ),
        dcc.Dropdown(
            id="category-dropdown",
            options=[{'label': yr, 'value': yr} for yr in year],
            style={"width": "300px",
                   "left": "100px",
                   "border-radius": "1px"},
            value="1934"  # Default value for dropdown
        ),

        html.Div(
            html.P(
                ["This Dashboard contains all the countries which participated in Football Worldcup thoughout the Years.",
                 html.Br(), "The Graph shows the Win and Loss percentage of country participated."],
                style={"text-align": "center"}
            ),  # Set background color and
        ),

        html.Div(children=[dcc.Graph(id="position", style={
            "display": "block", "position": "absolute", "right": "80px", "width": "50%"}),
            dcc.Graph(id="graph",
                      figure={
                          'layout': {
                              'plot_bgcolor': 'white',
                              'paper_bgcolor': 'white'
                          }}, style={"width": "40%", "left": "10px","margin": "0"})], style={"position": "relative", "text-align": "center",
                                                               "display": "grid"},
        )
    ]  # Set background color for the whole layout
)


@app.callback(
    dash.dependencies.Output('item-dropdown', 'options'),
    dash.dependencies.Output('item-dropdown', 'value'),
    [dash.dependencies.Input('category-dropdown', 'value')]
)
def update_dropdown(value):
    global df
    df = pd.read_csv(
        f'E:/Workspace/Data Science/Data Science Project/WC2023/archive/{value}.csv')
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
    filtered_df['WinPercentage'] = (
        filtered_df['Win'] / filtered_df['Games Played']) * 100
    filtered_df['LossPercentage'] = (
        filtered_df['Loss'] / filtered_df['Games Played']) * 100
    filtered_df['DrawPercentage'] = (
        filtered_df['Draw'] / filtered_df['Games Played']) * 100
    win_percentage = filtered_df['WinPercentage'].iloc[0]
    loss_percentage = filtered_df['LossPercentage'].iloc[0]
    draw_percentage = filtered_df['DrawPercentage'].iloc[0]
    fig = go.Figure(data=[go.Pie(labels=['Win', 'Loss', 'Draw'], values=[
                    win_percentage, loss_percentage, draw_percentage])])
    fig.update_layout(
        title={'text': f'Win-Loss Percentage for {selected_team}', 'x': 0.5})
    return fig


@app.callback(
    dash.dependencies.Output('position', 'figure'),
    [dash.dependencies.Input('item-dropdown', 'value')]
)
def timeseries(value):
    position = []
    years = []
    for i in range(len(data_path)):
        gdf = pd.read_csv(data_path[i])
        try:
            position.append(gdf[gdf['Team'] == value].iloc[:, 0].values[0])
            years.append(year[i])
        except:
            pass

    time_series_df = pd.DataFrame({'Position': position, "Years": years})
    fig = px.scatter(time_series_df, x='Years', y="Position", color="Position", range_y=[
                     0, 20], title=f"Finished Position of {value} throughout the years")
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0.1)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }, title_x=0.5)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
