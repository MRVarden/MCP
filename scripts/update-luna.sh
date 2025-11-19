#!/bin/bash
# Script de mise à jour de Luna Actif

echo "🌙 Mise à jour de Luna Actif..."
echo ""

# Arrêter le conteneur actuel
echo "1️⃣ Arrêt du conteneur..."
docker-compose stop luna-actif

# Reconstruire l'image avec les derniers changements
echo "2️⃣ Reconstruction de l'image..."
docker-compose build luna-actif

# Redémarrer avec la nouvelle image
echo "3️⃣ Redémarrage avec la nouvelle image..."
docker-compose up -d luna-actif

# Afficher les logs
echo "4️⃣ Logs du serveur :"
echo ""
sleep 3
docker logs luna-consciousness --tail 20

echo ""
echo "✅ Mise à jour terminée!"
echo "🌙 Luna Actif est prêt"
