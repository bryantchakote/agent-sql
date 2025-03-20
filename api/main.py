from dotenv import load_dotenv

from fastapi import FastAPI, Form

from pydantic import BaseModel, Field

from langchain import hub as prompts

from langchain_openai import ChatOpenAI

from langgraph.prebuilt import create_react_agent

from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit


# Variables d'environnement (clés API)
load_dotenv(".env.local", override=True)

# Initialisation de l'app
app = FastAPI()

# Connexion à la base de données
db = SQLDatabase.from_uri("sqlite:///db/Chinook.db")


# Agent
class SubmitFinalAnswer(BaseModel):
    """Formats the final agent response. Returns empty strings fields if necessary."""

    query: str = Field(
        description="The SQL query that may have been executed to obtain the answer (if applicable)."
    )
    result: str = Field(description="The result of the SQL query (if applicable).")
    answer: str = Field(description="The final answer to the user.")


llm = ChatOpenAI(model="gpt-4o-mini")
tools = SQLDatabaseToolkit(db=db, llm=llm).get_tools() + [SubmitFinalAnswer]
prompt = prompts.pull("agent-sql:93819056").format(dialect=db.dialect, top_k=5)
agent = create_react_agent(llm, tools, prompt=prompt)


@app.post("/answer")
async def answer(question: str = Form(...)):
    answer = agent.invoke({"messages": question})
    return {"answer": answer}
