# AI Agent Toolkit

This project implements a **modular AI Agent** using **LangChain**, featuring tools for:

- **Video Transcription** from YouTube
- **Transcription Summarization**
- **News Article Search** based on extracted keywords
- **Saving** agent outputs to a Markdown file

The agent accepts a list of instructions and orchestrates these tools to perform a full Retrieval-Augmented Generation (RAG) workflow.

---

## 📦 Project Structure

```text
.
├── src                 # Source folder
   ├── transcribe.py      # Tool to transcribe YouTube videos
   ├── news.py            # Tool to search news articles via API
   ├── llm.py             # LLM loader and invoker (Ollama/OpenAI)
   ├── agent.py           # Main script defining tools and running the agent
├── .env                # Environment variables (models, API keys, etc.)
├── requirements.txt    # Project dependencies
└── files/              # Directory for temporary files (transcriptions)
```

---

## ⚙️ Installation

1. **Clone the repository**:

   ```bash
   git clone <REPO_URL>
   cd <PROJECT_FOLDER>
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Create a `.env` file in the project root with:
   ```dotenv
   OLLAMA_API_URL=http://localhost:11434 # local ollama url
   NEWS_API_KEY=news_api_key
   CONVERSATION_MODEL=llama2    # or another supported model
   OPENAI_API_KEY=your_openai_key
   ```

---

## 🚀 Usage

Run the agent with:

```bash
python src/agent.py
```

The agent will execute the workflow defined in `run_agent()` and output Markdown to the console, as well as save the result to `agent_output.md`.

### Example Instructions

In `src/agent.py`, `text_input` is a list of tasks for the agent:

```python
text_input = [
  "Summarize the video at https://www.youtube.com/watch?v=...",
  "Search for 6 news articles related to the transcription.",
  "Save the summary, keywords and the news articles in Portuguese (pt-BR).",
]
```

Feel free to modify this list or read input dynamically for more flexibility.

---

## 🛠 Available Tools

| Tool                | Description                                              |
| ------------------- | -------------------------------------------------------- |
| `transcribe_tool`   | Transcribes the audio of a YouTube video                 |
| `summarize_tool`    | Summarizes the transcription into key bullet points      |
| `search_news_tools` | Extracts keywords and searches for related news articles |
| `save_tool`         | Saves the final response to `agent_output.md`            |

Each tool is decorated with `@tool` and returns a specific type, allowing the agent to call them dynamically.

---

## 📁 File Configuration

- **`files/`**: Folder where video transcriptions are temporarily stored.
- **`agent_output.md`**: Output file generated by the `save_tool`.

---

## 🔧 Customization

- **Models**: Change `CONVERSATION_MODEL` in `.env` to use different LLMs (e.g., `llama2`, `gpt-4o`).
- **Temperature**: Adjust the `temperature` parameter when loading models in `LLM.load_ollama_model` or `LLM.load_open_ai_model`.
- **Tools**: Add new functions decorated with `@tool` in `src/agent.py` and include them in the `toolkit` list.

---

## 📚 References

- [LangChain Documentation](https://langchain.com)
- [Ollama CLI & Server](https://ollama.com)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

---
