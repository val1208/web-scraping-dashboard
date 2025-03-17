import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Fichier CSV avec les prix
CSV_FILE = "../scraper/prices/bitcoin_prices.csv"


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Bitcoin Price Tracker 💰"),
    dcc.Graph(id="price-chart"),
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Mettre à jour toutes les 5 minutes
        n_intervals=0
    )
])

# mettre à jour le graphique
@app.callback(
    Output("price-chart", "figure"),
    Input("interval-update", "n_intervals")
)
def update_graph(n):
    try:
        df = pd.read_csv(CSV_FILE, names=["Date", "Price"], parse_dates=["Date"])
        df = df.sort_values(by="Date")  # Trier par date

        fig = px.line(df, x="Date", y="Price", title="Évolution du prix du Bitcoin")
        fig.update_traces(line=dict(color="gold", width=2))
        return fig
    except Exception as e:
        print("Erreur de lecture du CSV:", e)
        return px.line(title="Aucune donnée disponible")

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
