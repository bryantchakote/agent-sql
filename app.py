# %%
from dotenv import load_dotenv

# Chargement des clés API
load_dotenv("./.env.local", override=True)


# %%
from langchain_community.utilities import SQLDatabase

# Connexion à la base de données
db = SQLDatabase.from_uri("sqlite:///db/Chinook.db")


# %%
from langchain_openai import ChatOpenAI

# Modèle
llm = ChatOpenAI(model="gpt-4o-mini")


# %%
from langchain_community.agent_toolkits import SQLDatabaseToolkit

# Outils pour manipuler les bases de données
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
tools = toolkit.get_tools()


# %%
from langchain import hub

# Prompt
prompt_template = hub.pull("agent-sql")
prompt = prompt_template.format(dialect=db.dialect, top_k=5)


# %%
from langgraph.prebuilt import create_react_agent

# Initialisation de l'agent
agent_executor = create_react_agent(llm, tools, prompt=prompt)


# %%
# App Streamlit
from langchain_core.messages import AIMessage
import streamlit as st
import logging
import json

st.title("📝 Chatbot SQL Interactif")

# Initialisation de l'historique des messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Prompt utilisateur
question = st.chat_input("Posez une question sur la base de données...")

if question:
    with st.spinner("⚙️ En cours d'exécution..."):
        # Réponse brute
        response = agent_executor.invoke({"messages": question})

        # Dernier message
        final_response = response["messages"][-1]

        # Afficher si le dernier message vient du LLM
        if isinstance(final_response, AIMessage):
            # Récupération du résultat JSON (sous forme de chaîne)
            str_content = response["messages"][-1].content.strip("`|json")

            # Conversion en dictionnaire Python
            logging.basicConfig(level=logging.ERROR)

            try:
                content = json.loads(str_content)
            except json.JSONDecodeError as e:
                logging.error(f"Erreur de décodage JSON: {e}")
                raise ValueError("Le contenu fourni n'est pas un JSON valide.") from e
            except Exception as e:
                logging.error(f"Une erreur inattendue s'est produite : {e}")
                raise

            # Mise à jour de l'historique
            st.session_state.chat_history.append(
                {"question": question, "response": content}
            )
        else:
            ...

# Affichage de l'historique du chat
for chat in st.session_state.chat_history:
    # Message utilisateur
    st.chat_message("user").write(chat["question"])

    # Dictionnaire de réponse LLM
    response = chat["response"]

    # Réponse finale
    st.chat_message("assistant").write(response["answer"])

    # Toggles pour les détails (requête et résultats éventuels)
    with st.expander("🔍 Voir la requête SQL exécutée"):
        st.code(response["query"], language="sql")
    with st.expander("📊 Voir le résultat de la requête"):
        st.code(response["result"])

# %%
