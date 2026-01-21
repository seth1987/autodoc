#!/bin/bash
echo "========================================"
echo "   Démarrage AutoDoc"
echo "========================================"
echo

# Start backend in background
echo "Démarrage du backend..."
cd backend
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend in background
echo "Démarrage du frontend..."
cd frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!
cd ..

# Wait a bit
sleep 2

# Open browser (works on Mac and Linux)
echo "Ouverture du navigateur..."
if command -v open &> /dev/null; then
    open http://localhost:3000
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:3000
fi

echo
echo "========================================"
echo "   AutoDoc démarré !"
echo "========================================"
echo
echo "Backend  : http://localhost:8000"
echo "Frontend : http://localhost:3000"
echo
echo "Appuie sur Ctrl+C pour arrêter"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
