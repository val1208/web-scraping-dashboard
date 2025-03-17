#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Dossier où enregistrer les prix
OUTPUT_DIR="$SCRIPT_DIR/prices"
mkdir -p "$OUTPUT_DIR"

# Fichier CSV
CSV_FILE="/home/valen/projects/web-scraping-dashboard/scraper/prices/bitcoin_prices.csv"

# URL de l'API Bitstack
URL="https://api.bitstack-app.com/pricetagger/v1/stats/web?currency=EUR"

if ! command -v jq &> /dev/null; then
    echo "Erreur : jq n'est pas installé. Installez-le avec 'sudo apt install jq'."
    exit 1
fi


JSON=$(curl -s -H "User-Agent: Mozilla/5.0" "$URL")


if [[ -z "$JSON" ]]; then
    echo "Erreur : Impossible de récupérer les données."
    exit 1
fi

# Extraire le prix du Bitcoin en EUR
PRICE=$(echo "$JSON" | jq -r '.currentPrice')


DATE=$(date +"%Y-%m-%d %H:%M:%S")


if [[ -n "$PRICE" && "$PRICE" != "null" ]]; then
    echo "$DATE, $PRICE" >> "$CSV_FILE"
    echo "Valeur Bitcoin : $PRICE EUR"
else
    echo "Erreur : Impossible d'extraire la valeur du Bitcoin."
fi
