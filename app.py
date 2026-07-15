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


# =========================
# CONFIGURAÇÃO DA OPENAI
# =========================

load_dotenv()

api_key = os.getenv("api_key")
base_url = os.getenv('base_url')

if not api_key:
    raise ValueError(
        "A variável api_key não foi encontrada. "
        "Verifique se ela foi adicionada corretamente ao arquivo .env."
    )


llm = ChatOpenAI(
    model="gemini-3.1-flash-lite",
    api_key=api_key,
    base_url=base_url
)


# =========================
# PROMPT
# =========================

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Você é um assistente de viagem inteligente.

Ajude o usuário a planejar:

- roteiros de viagem;
- custos e orçamentos;
- destinos;
- passeios;
- cronogramas;
- hospedagens;
- meios de transporte;
- dicas práticas.

Apresente informações claras, organizadas e objetivas.

Quando não possuir informações suficientes, faça perguntas ao usuário
antes de elaborar o planejamento.

Responda sempre em português do Brasil.
"""
    ),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])


chain = prompt | llm | StrOutputParser()


# =========================
# HISTÓRICO DA CONVERSA
# =========================

store = {}


def get_session_history(session_id: str):
    """Retorna ou cria o histórico de uma sessão."""

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
# FUNÇÕES DA INTERFACE
# =========================

def enviar_mensagem():
    """Captura a pergunta e inicia o processamento em outra thread."""

    pergunta = entrada.get().strip()

    if not pergunta:
        return

    entrada.delete(0, tk.END)

    area_chat.config(state=tk.NORMAL)
    area_chat.insert(tk.END, f"Você: {pergunta}\n\n")
    area_chat.insert(tk.END, "Assistente: pensando...\n\n")
    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)

    botao_enviar.config(state=tk.DISABLED)
    entrada.config(state=tk.DISABLED)

    thread = threading.Thread(
        target=processar_resposta,
        args=(pergunta,),
        daemon=True
    )

    thread.start()


def processar_resposta(pergunta: str):
    """Envia a pergunta ao modelo da OpenAI."""

    try:
        resposta = chat.invoke(
            {"input": pergunta},
            config={
                "configurable": {
                    "session_id": "usuario_robert"
                }
            }
        )

    except Exception as erro:
        resposta = (
            "Não foi possível gerar a resposta.\n\n"
            f"Detalhes do erro: {erro}"
        )

    janela.after(0, atualizar_chat, resposta)


def atualizar_chat(resposta: str):
    """Atualiza a interface com a resposta do modelo."""

    area_chat.config(state=tk.NORMAL)

    conteudo = area_chat.get("1.0", tk.END)

    # Remove somente a última mensagem de processamento
    marcador = "Assistente: pensando...\n\n"
    posicao = conteudo.rfind(marcador)

    if posicao != -1:
        conteudo = (
            conteudo[:posicao]
            + conteudo[posicao + len(marcador):]
        )

    area_chat.delete("1.0", tk.END)
    area_chat.insert(tk.END, conteudo)
    area_chat.insert(tk.END, f"Assistente: {resposta}\n\n")

    area_chat.config(state=tk.DISABLED)
    area_chat.see(tk.END)

    botao_enviar.config(state=tk.NORMAL)
    entrada.config(state=tk.NORMAL)
    entrada.focus()


# =========================
# INTERFACE TKINTER
# =========================

janela = tk.Tk()
janela.title("Assistente de Viagem com OpenAI")
janela.geometry("700x500")


area_chat = scrolledtext.ScrolledText(
    janela,
    wrap=tk.WORD,
    font=("Arial", 11)
)

area_chat.pack(
    padx=10,
    pady=10,
    fill=tk.BOTH,
    expand=True
)

area_chat.config(state=tk.DISABLED)


frame_entrada = tk.Frame(janela)

frame_entrada.pack(
    padx=10,
    pady=(0, 10),
    fill=tk.X
)


entrada = tk.Entry(
    frame_entrada,
    font=("Arial", 12)
)

entrada.pack(
    side=tk.LEFT,
    fill=tk.X,
    expand=True
)

entrada.bind(
    "<Return>",
    lambda event: enviar_mensagem()
)


botao_enviar = tk.Button(
    frame_entrada,
    text="Enviar",
    command=enviar_mensagem
)

botao_enviar.pack(
    side=tk.RIGHT,
    padx=(5, 0)
)


entrada.focus()

janela.mainloop()