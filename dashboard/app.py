import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Fichier CSV avec les prix
CSV_FILE = "../scraper/prices/bitcoin_prices.csv"


app = dash.Dash(__name__)


app.layout = html.Div([
    html.H1("Bitcoin Price Tracker 💰"),
    dcc.Graph(id="price-chart"),
    html.Div(id="last-update", style={"padding": "10px", "fontSize": "18px", "fontWeight": "bold"}),
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Mettre à jour toutes les 5 minutes
        n_intervals=0
    )
])

# mettre à jour le graphique
@app.callback(
    [Output("price-chart", "figure"),
    Output("last-update", "children")],
    Input("interval-update", "n_intervals")
)
def update_graph(n):
    try:
        df = pd.read_csv(CSV_FILE, names=["Date", "Price"], parse_dates=["Date"])
        df = df.sort_values(by="Date")  # Trier par date
        
        df['Moving Average'] = df['Price'].rolling(window=7).mean()

        fig = px.line(df, x="Date", y="Price", title="Évolution du prix du Bitcoin avec Moyenne Mobile")
        
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Moving Average'], mode='lines', name='Moyenne Mobile', line=dict(color="blue", width=2)))

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Prix (USD)",
            template="plotly_dark"  
        )

        last_update = f"Dernière mis à jour: {df['Date'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')}"

        return fig, last_update
    except Exception as e:
        print("Erreur de lecture du CSV:", e)
        return px.line(title="Aucune donnée disponible")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
