# 📝 Agent-SQL : Chatbot SQL Interactif

Agent-SQL est une application interactive permettant d'exécuter des requêtes SQL en langage naturel grâce à LangChain et OpenAI. Elle prend en charge plusieurs bases de données et assure un contrôle strict sur l'exécution des requêtes.

## 🚀 Fonctionnalités

- Chatbot interactif avec prise en charge des requêtes SQL
- Prévention des requêtes dangereuses (`INSERT`, `UPDATE`, `DELETE`...)
- Interface utilisateur basée sur Streamlit
- Intégration avec OpenAI pour le traitement du langage naturel

## 📂 Structure du Projet

```
AGENT-SQL/
│── db/                     # Dossiers des bases de données
│   ├── Chinook.db          # Exemple de base SQLite
│   ├── ecommerce.db        # Base de données e-commerce
│   ├── northwind.db        # Base Northwind pour les tests
│
│── .env                    # Variables d'environnement
│── .gitignore              # Fichiers ignorés par Git
│── api.py                  # API pour interagir avec l'agent SQL
│── app.py                  # Application principale avec Streamlit
│── poetry.lock             # Fichier de dépendances Poetry
│── pyproject.toml          # Configuration Poetry
│── README.md               # Documentation du projet
```

## 🛠️ Installation

### 1️⃣ Prérequis

- Python 3.13+
- [Poetry](https://python-poetry.org/docs/)
- Clés API OpenAI et LangSmith (pour traquer l'utilisation du LLM)

### 2️⃣ Cloner le dépôt

```bash
git clone https://github.com/bryantchakote/agent-sql.git
cd agent-sql
```

### 3️⃣ Installer les dépendances

```bash
poetry install
```

### 4️⃣ Configurer les variables d'environnement

Créer un fichier `.env.local` et y ajouter :

```ini
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="lsv2_pt..."
LANGSMITH_PROJECT="agent-sql"
OPENAI_API_KEY="sk-proj-..."
```

### 5️⃣ Lancer l'application

```bash
poetry run streamlit run app.py
```
