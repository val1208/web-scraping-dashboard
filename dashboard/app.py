import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import subprocess
from sklearn.linear_model import LinearRegression


import os
import json
from datetime import datetime

def load_daily_report():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_dir, "..", "DailyReports")
    today = datetime.now().strftime("%Y-%m-%d")
    report_path = os.path.join(reports_dir, f"report-{today}.json")

    try:
        if os.path.exists(report_path):
            with open(report_path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"[ERREUR] Impossible de charger le rapport : {e}")
    
    return None



# Fichier CSV avec les prix
CSV_FILE = "../scraper/prices/bitcoin_prices.csv"

SCRAPER_SCRIPT = "../scraper/scraper.sh"

app = dash.Dash(__name__)


app.layout = html.Div([



    html.H1("Bitcoin Price Tracker "),
    dcc.Graph(id="price-chart"),
    dcc.Graph(id="price-distribution-chart"),
    html.Button("Récupérer les données du site", id="scrape-button", n_clicks=0),

	html.H2("Rapport journalier"),
	html.Div(id="daily-report", style={"marginTop": "20px"}),



    html.Div(id="last-update", style={"padding": "10px", "fontSize": "18px", "fontWeight": "bold"}),
    html.Div(id="last-values-table", style={"marginTop": "20px"}),    
    dcc.Interval(
        id="interval-update",
        interval=5 * 60 * 1000,  # Mettre à jour toutes les 5 minutes
        n_intervals=0
    ),
])

# mettre à jour le graphique
@app.callback(
    [Output("price-chart", "figure"),
    Output("price-distribution-chart", "figure"),
    Output("last-update", "children"),
    Output("last-values-table", "children"),
	Output("daily-report", "children")],
    [Input("interval-update", "n_intervals"),
    Input("scrape-button", "n_clicks")]
)

def update_graph(n_intervals, n_clicks):
    if n_clicks > 0:
        subprocess.run(["bash", SCRAPER_SCRIPT])
    try:
        df = pd.read_csv(CSV_FILE, names=["Date", "Price"], parse_dates=["Date"])
        df = df.sort_values(by="Date")
        df['Moving Average'] = df['Price'].rolling(window=7).mean()

        df['Timestamp'] = df['Date'].astype(np.int64) // 10**9  # Conversion de la date en timestamp
        X = df['Timestamp'].values.reshape(-1, 1) 
        y = df['Price'].values

        model = LinearRegression()
        model.fit(X, y)
        df['Prediction'] = model.predict(X)

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=df['Date'], y=df['Price'], mode='lines', name='Prix réel', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Moving Average'], mode='lines', name='Moyenne mobile (7 jours)', line=dict(color='green', dash='dot')))
        fig.add_trace(go.Scatter(x=df['Date'], y=df['Prediction'], mode='lines', name='Prédiction (Régression linéaire)', line=dict(color='red', dash='dash')))

        fig.update_layout(
            title="Évolution du prix du Bitcoin avec régression linéaire et moyenne mobile",
            xaxis_title="Date",
            yaxis_title="Prix (euro)",
            template="plotly_dark"
        )

        fig_distribution = px.histogram(df, x="Price", nbins=30, title="Distribution des prix du Bitcoin")
        fig_distribution.update_layout(xaxis_title="Prix (euro)", yaxis_title="Fréquence", template="plotly_dark")

        last_update = f"Dernière mise à jour: {df['Date'].iloc[-1].strftime('%Y-%m-%d %H:%M:%S')}"

        # Créer le tableau des 10 dernières valeurs
        last_10_values = df.tail(10)
        table = html.Table([
            html.Thead(html.Tr([html.Th("Date"), html.Th("Prix (euro)")]))
        ] + [
            html.Tr([html.Td(row['Date'].strftime('%Y-%m-%d %H:%M:%S')), html.Td(f"€{row['Price']:.2f}")])
            for _, row in last_10_values.iterrows()
        ])

        report = load_daily_report()
        if report:
            report_html = html.Ul([
                html.Li(f"Nombre de points: {report['count']}"),
                html.Li(f"Prix minimum: ${report['min']:.2f}"),
                html.Li(f"Prix maximum: ${report['max']:.2f}"),
                html.Li(f"Prix moyen: ${report['avg']:.2f}"),
                html.Li(f"Premier prix: ${report['first']:.2f}"),
                html.Li(f"Dernier prix: ${report['last']:.2f}"),
                html.Li(f"Période : {report['start_time']} → {report['end_time']}"),
            ])
        else:
            report_html = html.I("Aucun rapport journalier trouvé.")

        return fig, fig_distribution, last_update, table, report_html

    except Exception as e:
        print("Erreur de lecture du CSV:", e)
        return px.line(title="Aucune donnée disponible"), go.Figure(), "", "", html.I("Erreur de chargement des données.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8050, debug=True)
