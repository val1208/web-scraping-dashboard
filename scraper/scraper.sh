#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# URL de l'API à scraper
URL="https://cdn.cboe.com/api/global/delayed_quotes/quotes/_SPX.json"

# Récupérer les données JSON
JSON=$(curl -s -H "User-Agent: Mozilla/5.0" -H "Referer: https://www.cboe.com/" "$URL")

# Vérifier si la requête a réussi
if [[ -z "$JSON" ]]; then
    echo "Erreur : Impossible de récupérer les données."
    exit 1
fi

# Extraire la valeur de l'indice SPX
PRICE=$(echo "$JSON" | jq -r '.data.current_price')


# Récupérer la date actuelle
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifier si le prix a bien été extrait
if [[ -n "$PRICE" && "$PRICE" != "null" ]]; then
    echo "$DATE, $PRICE" >> prices.csv
    echo "Valeur SPX : $PRICE USD"
else
    echo "Erreur : Impossible d'extraire la valeur de l'indice SPX."
fi
