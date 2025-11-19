import streamlit as st
from utils import (
    fetch_newsapi_results,
    fetch_tavily_results,
    run_rag_pipeline,
)

st.set_page_config(page_title="News AI – Latest AI Updates", layout="wide")

st.title("🧠 News AI – Your AI Industry News Companion")

st.markdown(
    "Welcome to **News AI**.\n\n"
    "Ask anything about the **latest AI / Generative AI / ML trends**. "
    "News AI will call external news/search APIs (NewsAPI.org and/or Tavily), "
    "retrieve fresh articles, and summarize them for you using a RAG-style pipeline backed by an LLM."
)

default_query = "artificial intelligence OR generative AI"

query = st.text_input(
    "Your question or news query (leave empty to use a default AI news query):",
    placeholder=default_query,
)

st.sidebar.header("Source Configuration")

source = st.sidebar.selectbox(
    "Select news/search source:",
    ["NewsAPI.org", "Tavily", "Both (merge results)"],
)

st.sidebar.markdown(
    """### API Keys via .env

This project loads API keys from a local **.env** file using `python-dotenv`.

Expected variables:

- `NEWSAPI_KEY` – for NewsAPI.org
- `TAVILY_API_KEY` – for Tavily Search API
- `OPENAI_API_KEY` – for LLM summarization (OpenAI)

Create a `.env` file in the project root with these values.
"""
)

if st.button("Get Latest AI Updates"):
    user_query = query.strip() or default_query

    all_results = []

    with st.spinner("News AI is fetching the latest AI updates..."):
        if source in ("NewsAPI.org", "Both (merge results)"):
            newsapi_results = fetch_newsapi_results(user_query)
            all_results.extend(newsapi_results)

        if source in ("Tavily", "Both (merge results)"):
            tavily_results = fetch_tavily_results(user_query)
            all_results.extend(tavily_results)

    if not all_results:
        st.error(
            "No results returned. Check your API keys (NEWSAPI_KEY / TAVILY_API_KEY) "
            "and your network connectivity."
        )
    else:
        st.subheader("🔗 Retrieved Articles / Results")
        for i, r in enumerate(all_results, start=1):
            st.markdown(f"**{i}. [{r['title']}]({r['link']})**")
            if r.get("source_name"):
                st.caption(r["source_name"])
            st.write(r.get("snippet", ""))
            st.markdown("---")

        with st.spinner("News AI is generating a summarized view (RAG over results)..."):
            answer = run_rag_pipeline(user_query, all_results)

        st.subheader("📝 News AI Summary")
        st.write(answer)
