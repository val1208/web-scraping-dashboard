




import os
import csv
import json
from datetime import datetime


base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = "/home/ubuntu/web-scraping-dashboard/scraper/prices/bitcoin_prices.csv"

output_dir = os.path.join(base_dir, "DailyReports")
os.makedirs(output_dir, exist_ok=True)

today = datetime.now().strftime("%Y-%m-%d")
output_path = os.path.join(output_dir, f"report-{today}.json")

try:
    # Lecture du fichier CSV
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if len(rows) < 2:
        print("[WARN] CSV vide ou pas de données.")
        exit()

    prices = []
    timestamps = []

    for row in rows:
        try:
            timestamp = row[0]
            price = float(row[1])
            timestamps.append(timestamp)
            prices.append(price)
        except (IndexError, ValueError):
            continue

    if not prices:
        print("[WARN] Aucune donnée valide trouvée.")
        exit()

    # Création du rapport
    report = {
        "count": len(prices),
        "min": min(prices),
        "max": max(prices),
        "avg": round(sum(prices) / len(prices), 2),
        "first": prices[0],
        "last": prices[-1],
        "start_time": timestamps[0],
        "end_time": timestamps[-1],
    }

    # Sauvegarde du rapport en JSON
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[OK] Rapport généré : {output_path}")

except FileNotFoundError:
    print(f"[ERREUR] Fichier introuvable : {csv_path}")
except Exception as e:
    print(f"[ERREUR] {e}")
