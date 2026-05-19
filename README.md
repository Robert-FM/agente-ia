# 🌍 Assistente de Viagem com IA

Um assistente virtual desenvolvido em **Python** utilizando **Tkinter**, **LangChain** e integração com modelos de linguagem via **OpenRouter API**.

O projeto permite criar uma interface gráfica simples e funcional para interação com Inteligência Artificial em tempo real.

---

## 🚀 Funcionalidades

- ✅ Interface gráfica desktop com Tkinter
- ✅ Conversa em tempo real com IA
- ✅ Histórico de mensagens com memória de contexto
- ✅ Integração com modelos LLM via OpenRouter
- ✅ Processamento assíncrono usando Threads
- ✅ Estrutura simples e escalável

---

## 🛠️ Tecnologias Utilizadas

- Python 3.11+
- Tkinter
- LangChain
- OpenRouter API
- dotenv
- Threading

---

## 📂 Estrutura do Projeto

```bash
AGENTE-IA/
│
├── .venv/
├── .env
├── .gitignore
├── .python-version
├── app.py
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock
```

---

## ⚙️ Configuração do Ambiente

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/agente-ia.git
```

---

### 2️⃣ Acesse a pasta

```bash
cd agente-ia
```

---

### 3️⃣ Crie o ambiente virtual

#### Linux / MacOS

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 4️⃣ Instale as dependências

Caso utilize **uv**:

```bash
uv sync
```

Ou usando pip:

```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
OPENROUTER_API_KEY=sua_api_key
link=https://openrouter.ai/api/v1
```

---

## ▶️ Executando o Projeto

```bash
python app.py
```

---

## 🧠 Como Funciona

O sistema utiliza:

- **LangChain** para gerenciamento do fluxo conversacional
- **RunnableWithMessageHistory** para memória de contexto
- **Tkinter** para interface gráfica
- **Threads** para evitar travamentos na interface durante as respostas da IA

---

## 📸 Interface

A aplicação possui:

- Área de conversa
- Campo para envio de mensagens
- Respostas em tempo real
- Histórico de interação

---

## 📌 Exemplo de Uso

```text
Usuário: Quero viajar para Gramado em julho.

Assistente:
Gramado é uma ótima opção no inverno! Aqui estão algumas dicas...
```

---

## 📈 Melhorias Futuras

- [ ] Tema escuro
- [ ] Integração com APIs de clima
- [ ] Sistema de voz
- [ ] Histórico salvo em banco de dados
- [ ] Streaming de respostas
- [ ] Upload de imagens e PDFs
- [ ] Integração com mapas

---

## 🤝 Contribuição

Contribuições são bem-vindas!

Sinta-se à vontade para abrir:
- Issues
- Pull Requests
- Sugestões

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

Robert Melo

🔗 LinkedIn: https://linkedin.com  
🐍 Python | IA | Machine Learning | LangChain | Data Science