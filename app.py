import os
import threading
import tkinter as tk
from tkinter import scrolledtext
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
link = os.getenv('link')

llm = ChatOpenAI(
    model="deepseek/deepseek-v4-flash:free",
    api_key=api_key,
    base_url=link,
    temperature=0.7,
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """
Você é um assistente de viagem inteligente.
Ajude o usuário a planejar roteiros, custos, destinos, passeios,
cronogramas e dicas práticas.

Responda sempre em português do Brasil.
"""),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm | StrOutputParser()

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chat = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)


# =========================
# INTERFACE TKINTER
# =========================

def enviar_mensagem():
    pergunta = entrada.get().strip()

    if not pergunta:
        return

    entrada.delete(0, tk.END)

    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"Você: {pergunta}\n\n")
    area_chat.insert(tk.END, "Assistente: pensando...\n\n")
    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)

    threading.Thread(
        target=processar_resposta,
        args=(pergunta,),
        daemon=True
    ).start()


def processar_resposta(pergunta):
    try:
        resposta = chat.invoke(
            {"input": pergunta},
            config={"configurable": {"session_id": "usuario_robert"}}
        )
    except Exception as e:
        resposta = f"Erro ao gerar resposta: {e}"

    janela.after(0, atualizar_chat, resposta)


def atualizar_chat(resposta):
    area_chat.config(state=tk.NORMAL)

    conteudo = area_chat.get("1.0", tk.END)
    conteudo = conteudo.replace("Assistente: pensando...\n\n", "")

    area_chat.delete("1.0", tk.END)
    area_chat.insert(tk.END, conteudo)
    area_chat.insert(tk.END, f"Assistente: {resposta}\n\n")

    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)


janela = tk.Tk()
janela.title("Assistente de Viagem com IA")
janela.geometry("700x500")

area_chat = scrolledtext.ScrolledText(
    janela,
    wrap=tk.WORD,
    font=("Arial", 11)
)
area_chat.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
area_chat.config(state=tk.DISABLED)

frame_entrada = tk.Frame(janela)
frame_entrada.pack(padx=10, pady=10, fill=tk.X)

entrada = tk.Entry(frame_entrada, font=("Arial", 12))
entrada.pack(side=tk.LEFT, fill=tk.X, expand=True)
entrada.bind("<Return>", lambda event: enviar_mensagem())

botao_enviar = tk.Button(
    frame_entrada,
    text="Enviar",
    command=enviar_mensagem
)
botao_enviar.pack(side=tk.RIGHT, padx=5)

janela.mainloop()