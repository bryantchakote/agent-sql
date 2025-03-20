# App Streamlit
import requests
from langchain_core.messages import AIMessage
import streamlit as st
import logging
import json
import re

st.title("📝 Chatbot SQL Interactif")

# Initialisation de l'historique des messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Prompt utilisateur
question = st.chat_input("Posez une question sur la base de données...")

if question:
    with st.spinner("⚙️ En cours d'exécution..."):
        # Réponse brute
        response = requests.post(
            "http://127.0.0.1:8000/answer", data={"question": question}
        )

        if response.status_code == 200:
            # Récupération du résultat (avant-dernier message)
            content = response.json().get("answer")["messages"][-2]["content"]
        else:
            st.error("Erreur lors de l'exécution de la requête.")
            logging.error(
                f"Erreur lors de l'exécution de la requête. {response.status_code}"
            )

        # Conversion en dictionnaire Python
        logging.basicConfig(level=logging.ERROR)

        # Extraction des valeurs
        pattern = r"query='(.*?)'\s+result='(.*?)'\s+answer='(.*?)'"
        match = re.search(pattern, content)

        if match:
            query = match.group(1)
            result = match.group(2)
            answer = match.group(3)
        else:
            # Si l'agent ne renvoie pas les données au bon format, on récupère juste sa réponse finale
            query = ""
            result = ""
            answer = response.json().get("answer")["messages"][-1]["content"]

        # Mise à jour de l'historique
        st.session_state.chat_history.append(
            {"question": question, "query": query, "result": result, "answer": answer}
        )

# Affichage de l'historique du chat
for chat in st.session_state.chat_history:
    st.chat_message("user").write(chat["question"])
    st.chat_message("assistant").write(chat["answer"])

    # Toggles pour les détails (requête et résultats éventuels)
    with st.expander("🔍 Voir la requête exécutée"):
        st.code(chat["query"], language="sql")
    with st.expander("📊 Voir le résultat de la requête"):
        st.code(chat["result"])
