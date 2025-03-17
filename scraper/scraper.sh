#!/bin/bash
export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

# URL de la page à scraper
URL="https://www.investing.com/equities/apple-computer-inc"

# Récupérer le contenu de la page
HTML=$(curl -s -H "User-Agent: Mozilla/5.0" "$URL")

# Extraire le prix de l'action Apple en utilisant une regex plus robuste
PRICE=$(echo "$HTML" | grep -oP '(?<=data-test="instrument-price-last">)\s*[0-9]+(\.[0-9]+)?')

# Récupérer la date actuelle
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# Vérifier si le prix a bien été extrait
if [[ -n "$PRICE" ]]; then
    PRICE=$(echo "$PRICE" | tr -d '[:space:]')  # Supprimer les espaces éventuels
    echo "$DATE, $PRICE" >> prices.csv
    echo "Prix Apple : $PRICE USD"
else
    echo "Erreur : Impossible d'extraire le prix."
fi
