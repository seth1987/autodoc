#!/bin/bash
echo "========================================"
echo "   Installation AutoDoc"
echo "========================================"
echo

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "[ERREUR] Python 3 n'est pas installé."
    echo "Installe Python : https://www.python.org/downloads/"
    exit 1
fi
echo "[OK] Python détecté"

# Install backend dependencies
echo
echo "Installation des dépendances backend..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "[ERREUR] Échec de l'installation des dépendances"
    exit 1
fi
echo "[OK] Dépendances installées"

# Install Playwright browser
echo
echo "Installation du navigateur Playwright (pour PDF)..."
playwright install chromium
echo "[OK] Playwright installé"

cd ..

echo
echo "========================================"
echo "   Installation terminée !"
echo "========================================"
echo
echo "Pour lancer l'application : ./start.sh"
