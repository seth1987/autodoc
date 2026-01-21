# AutoDoc

Convertisseur de documents PDF/DOCX en rapports HTML professionnels.

## Fonctionnalités

- **Conversion PDF/DOCX** : Extrait le texte et la structure des documents
- **Analyse LLM** : Utilise un LLM pour détecter les composants (titres, callouts, tableaux, etc.)
- **Génération HTML** : Produit un HTML autonome avec CSS intégré
- **Multi-providers** : Supporte OpenAI, Anthropic, et serveurs locaux (LM Studio, Ollama)
- **Interface web** : Interface simple et intuitive

## Structure du projet

```
autodoc/
├── backend/
│   ├── app/
│   │   ├── main.py              # API FastAPI
│   │   ├── config.py            # Configuration
│   │   ├── models.py            # Modèles Pydantic
│   │   ├── extractors/          # Extraction PDF/DOCX
│   │   ├── services/            # LLM, Converter, HTML Generator
│   │   └── templates/           # Template CSS
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── tests/
```

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

### Lancement

```bash
# Backend (depuis le dossier backend)
uvicorn app.main:app --reload --port 8000

# Frontend (servir les fichiers statiques)
# Option 1: Python
cd frontend && python -m http.server 3000

# Option 2: Node.js
npx serve frontend -p 3000
```

## Configuration

### Providers LLM

| Provider | Configuration |
|----------|---------------|
| **OpenAI** | Clé API (sk-...) + modèle (gpt-4, gpt-4o, etc.) |
| **Anthropic** | Clé API (sk-ant-...) + modèle (claude-3-5-sonnet, etc.) |
| **Custom** | URL (ex: http://localhost:1234) + modèle |

### LM Studio (local, gratuit)

1. Télécharger [LM Studio](https://lmstudio.ai/)
2. Charger un modèle (ex: Llama 3, Mistral)
3. Démarrer le serveur local
4. Dans AutoDoc : Provider = Custom, URL = http://localhost:1234

## Utilisation

1. Ouvrir l'interface web (http://localhost:3000)
2. Configurer le provider LLM et la clé API
3. Uploader un fichier PDF ou DOCX
4. Cliquer sur "Convertir"
5. Télécharger le HTML généré

## API Endpoints

| Endpoint | Méthode | Description |
|----------|---------|-------------|
| `/` | GET | Info API |
| `/health` | GET | Health check |
| `/convert` | POST | Conversion document → HTML (JSON response) |
| `/convert/download` | POST | Conversion document → HTML (file download) |

### Exemple d'appel API

```bash
curl -X POST http://localhost:8000/convert \
  -F "file=@document.pdf" \
  -F 'llm_config={"provider":"openai","api_key":"sk-...","model":"gpt-4"}'
```

## Composants HTML supportés

Le HTML généré inclut les composants suivants :

- **Cover** : Page de couverture
- **TOC** : Table des matières
- **Sections** : Numérotation automatique (01, 02...)
- **Callouts** : Note, Success, Warning, Alert, Info
- **Listes** : À puces, numérotées, checklists
- **Tableaux** : Avec style
- **Citations** : Bloc stylisé
- **Timeline** : Chronologie verticale
- **Cards** : Grille de cartes
- **Stats** : Bloc de statistiques
- **Conclusion** : Section finale
- **Sources** : Bibliographie

## Limitations

- Les images sont ignorées (texte uniquement)
- Documents très complexes peuvent nécessiter un modèle LLM puissant
- La qualité dépend du modèle LLM utilisé

## Tests

```bash
cd backend
pytest tests/ -v
```

## Licence

MIT
