# Installation AutoDoc en Local

## Prérequis
- Python 3.10+ installé ([télécharger](https://www.python.org/downloads/))
- Git installé ([télécharger](https://git-scm.com/downloads))

---

## Installation Automatique (Recommandé)

### Windows
1. Télécharge le projet : `git clone https://github.com/seth1987/autodoc.git`
2. Double-clique sur `install.bat`
3. Attends la fin de l'installation
4. Double-clique sur `start.bat` pour lancer l'application

### Mac / Linux
1. Télécharge le projet : `git clone https://github.com/seth1987/autodoc.git`
2. Ouvre un terminal dans le dossier
3. Lance : `chmod +x install.sh start.sh && ./install.sh`
4. Lance : `./start.sh` pour démarrer l'application

---

## Installation Manuelle

### 1. Clone le projet
```bash
git clone https://github.com/seth1987/autodoc.git
cd autodoc
```

### 2. Installe les dépendances
```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

### 3. Lance le backend
```bash
uvicorn app.main:app --reload --port 8000
```

### 4. Lance le frontend (nouveau terminal)
```bash
cd frontend
python -m http.server 3000
```

### 5. Utilise l'application
Ouvre http://localhost:3000 dans ton navigateur.

---

## Utilisation

1. **Provider** : Choisis Custom (LM Studio) ou OpenAI/Anthropic
2. **URL API** : `http://localhost:1234` pour LM Studio local
3. **Clé API** : Laisse vide pour LM Studio, ou entre ta clé OpenAI/Anthropic
4. **Upload** : Sélectionne un fichier PDF ou DOCX
5. **Convertir** : Clique sur le bouton et attends le résultat

---

## Dépannage

### "Erreur de connexion au serveur"
→ Vérifie que le backend tourne sur le port 8000

### "Erreur lors de la conversion"
→ Vérifie que LM Studio tourne et qu'un modèle est chargé

### PDF ne génère pas
→ Vérifie que Playwright est installé : `playwright install chromium`
