import os
import requests
from typing import List, Dict

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file (if present)
load_dotenv()

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ---------- Fetch from NewsAPI.org ----------

def fetch_newsapi_results(query: str, page_size: int = 5) -> List[Dict]:
    """Fetch latest AI-related news using NewsAPI.org.

    Docs: https://newsapi.org/docs/endpoints/everything
    """
    if not NEWSAPI_KEY:
        print("NEWSAPI_KEY is not set")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": NEWSAPI_KEY,
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Error calling NewsAPI:", e)
        return []

    articles = data.get("articles", [])
    results: List[Dict] = []
    for art in articles:
        results.append(
            {
                "title": art.get("title", ""),
                "link": art.get("url", ""),
                "snippet": art.get("description", "") or "",
                "source_name": art.get("source", {}).get("name", "NewsAPI.org"),
            }
        )
    return results


# ---------- Fetch from Tavily Search API ----------

def fetch_tavily_results(query: str, max_results: int = 5) -> List[Dict]:
    """Use Tavily Search API to get AI-related web/news results.

    Docs: https://docs.tavily.com
    """
    if not TAVILY_API_KEY:
        print("TAVILY_API_KEY is not set")
        return []

    url = "https://api.tavily.com/search"
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results,
        "search_depth": "basic",
        "topic": "news",
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print("Error calling Tavily API:", e)
        return []

    results: List[Dict] = []
    for item in data.get("results", []):
        url_item = item.get("url", "")
        source_name = ""
        if url_item:
            try:
                source_name = url_item.split("/")[2]
            except Exception:
                source_name = "Tavily"

        results.append(
            {
                "title": item.get("title", ""),
                "link": url_item,
                "snippet": (item.get("content", "") or "")[:400],
                "source_name": source_name or "Tavily",
            }
        )
    return results


# ---------- RAG-style pipeline utilities ----------

def build_context_from_results(results: List[Dict]) -> str:
    """Builds a single context string from merged results for RAG-style use."""
    chunks = []
    for r in results:
        chunks.append(
            f"Source: {r.get('source_name', '')}\n"
            f"Title: {r.get('title', '')}\n"
            f"URL: {r.get('link', '')}\n"
            f"Snippet: {r.get('snippet', '')}\n"
        )
    return "\n---\n".join(chunks)


def call_llm(prompt: str) -> str:
    """Call OpenAI Chat Completions API to summarize the news context.

    Make sure OPENAI_API_KEY is set in your .env file.
    """
    if not OPENAI_API_KEY:
        return (
            "OPENAI_API_KEY is not set. Please add it to your .env file "
            "to enable News AI summaries."
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",  # choose any available chat model
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are 'News AI', an assistant that summarizes AI / Generative AI news "
                        "clearly and concisely for the user."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI LLM: {e}"


def run_rag_pipeline(query: str, results: List[Dict]) -> str:
    """Simple RAG-style pipeline:

    1. Use NewsAPI / Tavily (or both) as retrieval.
    2. Construct a context string from results.
    3. Send to an LLM for summarization.
    """
    context = build_context_from_results(results)

    prompt = f"""You are an assistant called 'News AI' that summarizes the latest
AI and Generative AI news and connects it to the user's question.

User question:
{query}

Aggregated news results:
{context}

Task:
- Summarize the most important AI-related updates.
- Highlight concrete products, models, companies, or research efforts.
- Point out any noticeable trends (e.g., regulatory changes, funding, new models).
- Keep the answer concise but informative.
"""

    answer = call_llm(prompt)
    return answer
