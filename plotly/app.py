import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd  # Import pandas
import glob
import plotly.express as px
import plotly.graph_objs as go

app = dash.Dash(__name__)

data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(data_path[-1])
    
teams = df_2022['HOST']
year = [x.split('\\')[-1].split('.csv')[0] for x in data_path][:-1]
df = None



app.layout = html.Div([
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
        style={"width": "200px",
               "left":"100px"},
        value="1934"  # Default value for dropdown
    ),
    html.Div(id='output-div', style= {"text-align": "center"}),
    dcc.Graph(id="graph"),
    html.Div(html.P(["This Dashboard contains all the countries which participated in Football Worldcup thoughout the Years.",html.Br(), "The Graph shows the Win and Loss percentage of country participated."],
           style= {"text-align": "center"}))
])



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

# @app.callback(
#     dash.dependencies.Output('output-div', 'children'),
#     [dash.dependencies.Input('item-dropdown', 'value')]
# )
# def update_output(selected_item):
#     return f'You selected: {selected_item}'


@app.callback(
    dash.dependencies.Output('graph', 'figure'),
    [dash.dependencies.Input('item-dropdown', 'value')]
)
def update_graph(selected_team):
    global df
    filtered_df = df[df['Team'] == selected_team]
    filtered_df['WinPercentage'] = (filtered_df['Win'] / filtered_df['Games Played']) * 100
    filtered_df['LossPercentage'] = (filtered_df['Loss'] / filtered_df['Games Played']) * 100
    win_percentage = filtered_df['WinPercentage'].iloc[0]
    loss_percentage = filtered_df['LossPercentage'].iloc[0]
    
    # fig = px.pie(names=['Win', 'Loss'], values=[win_percentage, loss_percentage],
    #              title=f'Win-Loss Percentage for {selected_team}', hole=0.3),
    # fig.update_layout(title_x=0.5)
    fig = go.Figure(data=[go.Pie(labels=['Win', 'Loss'], values=[win_percentage, loss_percentage])])
    # fig = go.Figure(fig)
    
    fig.update_layout(title={'text': f'Win-Loss Percentage for {selected_team}', 'x': 0.5})
    return fig


if __name__ == '__main__':
    app.run_server(host =" 192.168.0.1",port = 8050, debug=True)
