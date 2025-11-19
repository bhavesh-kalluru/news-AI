# 🧠 News AI – AI Industry News Companion

News AI is a Streamlit web app that fetches the **latest AI / Generative AI / ML news**
from external APIs (NewsAPI.org and Tavily) and summarizes it using an OpenAI LLM
in a simple **RAG-style** pipeline.

## ✨ Features

- Query **latest AI / GenAI / ML trends**
- Choose data source:
  - `NewsAPI.org`
  - `Tavily`
  - or **Both** (merged)
- Aggregates titles + links + snippets into a context
- Uses OpenAI Chat Completions to generate a **News AI Summary**
- Uses a `.env` file (via `python-dotenv`) so you don’t type keys every time

---

## 🧱 Tech Stack

- **Python**
- **Streamlit** – web UI
- **NewsAPI.org** – news articles
- **Tavily Search API** – web/news search optimized for AI use
- **OpenAI** – LLM summarization
- **python-dotenv** – loads API keys from `.env`

---

## 🔧 Setup

### 1. Clone the repo (after you push it to GitHub)

```bash
git clone https://github.com/<your-username>/news-ai.git
cd news-ai

