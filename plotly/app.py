import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import glob


### Here are some of the Ideas to look for
## Make a chloropleth map to show the countries participated in WC 2022 and their key metrices
## Create Heatmap for Most goals scored by different teams thorughout the history



### dataframe path
data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(data_path[-1])

app = dash.Dash(__name__)

# Make Chloropleth Map
app.layout = html.Div(style={"textAlign": "center"},
    children=[html.H1("Football Host Countries"),
    dcc.Graph(id = "wc-map",
              figure = {"layout": 
              {"height": 650,  # Adjust the height here
              "width": 1300,   # Adjust the width here
              }
            })
])

@app.callback(
    dash.dependencies.Output('wc-map', 'figure'),
    [dash.dependencies.Input('wc-map', 'clickData')]
)

def update_map(clickData):
    fig = px.choropleth(
        df_2022,
        locations= "HOST",
        locationmode='country names',
        color= "YEAR",
        hover_name= "HOST",
        projection= "natural earth",
        color_continuous_scale=px.colors.sequential.Plasma,
        scope='world'
    )

    if clickData:
        selected_country = clickData['points'][0]['location']
        fig.update_traces(marker=dict(color='red'), selector=dict(location=selected_country))

    return fig

if __name__ == '__main__':
    app.run_server(debug = True)
