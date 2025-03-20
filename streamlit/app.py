import streamlit as st
import requests
import logging
import json


# Nom de l'application
st.title("📝 Chatbot SQL Interactif")

# Initialisation de l'historique des messages
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Question de l'utilisateur
question = st.chat_input("Posez une question sur la base de données...")

if question:
    with st.spinner("⚙️ En cours d'exécution..."):
        # Réponse brute
        response = requests.post(
            "http://127.0.0.1:8000/answer", data={"question": question}
        )

        if response.status_code == 200:
            # Récupération du résultat
            content = (
                response.json().get("answer")["messages"][-1]["content"].strip("`|json")
            )
        else:
            logging.error(
                f"Erreur lors de l'exécution de la requête. Statut : {response.status_code}"
            )

        # Initialisation des composants de la réponse
        # Ce seront les valeurs finales si l'agent ne renvoie pas les données au bon format
        query = result = ""
        answer = content

        try:
            # Extraction des valeurs
            content = json.loads(content)

            query = content["query"]
            result = content["result"]
            answer = content["answer"]

        except json.JSONDecodeError as e:
            logging.error(f"Erreur de décodage JSON : {e}")

        except KeyError as e:
            logging.error(f"Erreur de clé JSON : {e}")

        except Exception as e:
            logging.error(f"Erreur inattendue : {e}")
            raise

        # Mise à jour de l'historique
        st.session_state.chat_history.append(
            {"question": question, "query": query, "result": result, "answer": answer}
        )

# Affichage de l'historique du chat
for chat in st.session_state.chat_history:
    st.chat_message("user").write(chat["question"])
    st.chat_message("assistant").write(chat["answer"])

# Toggles pour les détails (requête et résultats éventuels)
if st.session_state.chat_history:
    if st.session_state.chat_history[-1]["query"]:
        with st.expander("🔍 Requête"):
            st.code(chat["query"], language="sql")
        with st.expander("📊 Résultat"):
            st.code(chat["result"], language="txt")
