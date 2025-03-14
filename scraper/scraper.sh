#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# URL de la page à scraper
URL="https://www.investing.com/equities/apple-computer-inc"

# Scraper la page et extraire le prix de l'action Apple
PRICE=$(curl -s -H "User-Agent: Mozilla/5.0" "$URL" | grep -oP '(?<=data-test="instrument-price-last">)[0-9]+\.[0-9]+')

# Récupérer la date actuelle
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifier si le prix a bien été extrait
if [[ -n "$PRICE" ]]; then
    echo "$DATE, $PRICE" >> prices.csv
    echo "Prix Apple : $PRICE USD"
else
    echo "Erreur : Impossible d'extraire le prix."
fi
