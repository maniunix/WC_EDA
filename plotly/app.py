import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import glob

### dataframe path
data_path = glob.glob("archive/*.csv")
df_2022 = pd.read_csv(data_path[-1])

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1(children="WC Analysis"),  # Added a comma after this line
        html.P(
            children=(
                "Analyse the Historical Football WC Data"
            ),
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_2022['YEAR'],
                        "y": df_2022['GOALS SCORED'],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Goal Scored per Year "}
            },
        ),
        dcc.Graph(
            figure={
                "data": [
                    {
                        "x": df_2022['YEAR'],
                        "y": df_2022['GOALS SCORED'],
                        "type": "lines",
                    },
                ],
                "layout": {"title": "Goal Scored per Year "}
            },
        ),
    ]
)



if __name__ == "__main__":
    app.run_server(debug=True)