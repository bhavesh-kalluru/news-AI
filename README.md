# News AI 🧠

News AI is a Streamlit-based web application that aggregates the latest
Artificial Intelligence and Generative AI news from external APIs
and summarizes it using an OpenAI-powered LLM in a simple
Retrieval-Augmented Generation (RAG) style workflow.

---

## Features

- Fetches recent AI / Generative AI / ML news from:
  - **NewsAPI.org**
  - **Tavily Search API**
  - or both combined
- Displays article titles, sources, links, and snippets
- Builds a merged context from retrieved articles
- Generates a concise, LLM-based summary (“News AI Summary”)
- Uses a `.env` file for API keys (no need to re-enter them every run)

---

## Architecture Overview

1. **User Input**  
   The user provides a query (or uses a default AI-related query) in the Streamlit UI.

2. **Retrieval Layer**  
   Depending on the selected source:
   - `fetch_newsapi_results` calls NewsAPI.org.
   - `fetch_tavily_results` calls the Tavily Search API.
   - Results can be merged when both sources are selected.

3. **Context Building**  
   Retrieved articles (title, URL, snippet, source) are combined into a single
   context string suitable for LLM consumption.

4. **Generation Layer (RAG-style)**  
   The query + aggregated context are passed to an OpenAI Chat Completions model
   via `call_llm`, producing a summarized view of the latest AI news.

5. **Presentation**  
   Streamlit renders:
   - The raw retrieved results list
   - A synthesized “News AI Summary” for the user

---

## Tech Stack

- **Language:** Python
- **Web Framework:** Streamlit
- **Retrieval APIs:**
  - NewsAPI.org
  - Tavily Search API
- **LLM Provider:** OpenAI Chat Completions API
- **Config Management:** `python-dotenv` for `.env` loading

---

## Requirements

- Python 3.9+ (recommended)
- Valid API keys for:
  - [NewsAPI.org](https://newsapi.org/)
  - [Tavily](https://tavily.com/)
  - [OpenAI](https://platform.openai.com/)

---

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/news-ai.git
   cd news-ai
Create and activate a virtual environment (optional but recommended)

bash
Copy code
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
# venv\Scripts\activate.bat   # Windows (Command Prompt)
Install dependencies

bash
Copy code
pip install -r requirements.txt
Configuration (.env)
The application expects API keys to be provided via a .env file in the project root.

An example is provided as .env.example:

env
Copy code
NEWSAPI_KEY=your_newsapi_key_here
TAVILY_API_KEY=your_tavily_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
Create your actual .env file:

bash
Copy code
cp .env.example .env
Then edit .env and replace the placeholder values with your real keys.

Note: .env is listed in .gitignore and will not be committed to version control.

Running the Application
From the project root:

bash
Copy code
streamlit run app.py
Streamlit will print a local URL, typically:

text
Copy code
http://localhost:8501
Open it in your browser.

Usage
Open the app in your browser.

Enter a query about AI / Generative AI / ML (or leave it blank to use the default).

Select the source:

NewsAPI.org

Tavily

Both (merge results)

Click “Get Latest AI Updates”.

Review:

The list of retrieved articles and links.

The “News AI Summary” generated from the combined context.

Project Structure
text
Copy code
.
├── app.py            # Streamlit UI
├── utils.py          # NewsAPI + Tavily + OpenAI + RAG logic
├── requirements.txt  # Python dependencies
├── .env.example      # Example environment variables
└── .gitignore        # Excludes .env, venv, cache files, etc.# 🧠 News AI – AI Industry News Companion

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

