#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# URL de l'API ZoneBourse pour récupérer les données du S&P 500
URL="https://www.zonebourse.com/mods_a/charts/TV/function/history?from=1741881600&to=1742313600&symbol=4985&resolution=D&requestType=GET&src=itfp"

# Récupérer les données JSON
JSON=$(curl -s -H "User-Agent: Mozilla/5.0" "$URL")

# Vérifier si la requête a réussi
if [[ -z "$JSON" ]]; then
    echo "Erreur : Impossible de récupérer les données."
    exit 1
fi

# Vérifier si `jq` est installé
if ! command -v jq &> /dev/null; then
    echo "Erreur : jq n'est pas installé. Installez-le avec 'sudo apt install jq'."
    exit 1
fi

# Extraire la dernière valeur de clôture ("c" pour close)
PRICE=$(echo "$JSON" | jq -r '.c[-1]')

# Récupérer la date actuelle
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifier si le prix a bien été extrait
if [[ -n "$PRICE" && "$PRICE" != "null" ]]; then
    echo "$DATE, $PRICE" >> snp500_prices.csv
    echo "Valeur du S&P 500 : $PRICE USD"
else
    echo "Erreur : Impossible d'extraire la valeur de clôture du S&P 500."
fi
