import openai
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
OPENAI_API_KEY = os.getenv("openai_api_key")
GROQ_API_KEY = os.getenv("groq_api_key")

def groq_summarize(client, text, style, num_points=5):
    if style == "bullet":
        prompt = f"Summarize the following text in {num_points} concise bullet points:\n\n{text}"
    elif style == "abstract":
        prompt = f"Write a concise abstract (max {num_points} sentences) for the following article:\n\n{text}"
    elif style == "simple":
        prompt = f"Summarize this for a 12-year-old in {num_points} simple sentences:\n\n{text}"
    else:
        raise ValueError("Unknown style")
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a clear, factual summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_completion_tokens=350
    )
    return completion.choices[0].message.content.strip()

def openai_summarize(text, style, num_points=5, api_key=None):
    if api_key is None:
        api_key = OPENAI_API_KEY
    openai.api_key = api_key
    if style == "bullet":
        prompt = f"Summarize the following text in {num_points} concise bullet points:\n\n{text}"
    elif style == "abstract":
        prompt = f"Write a concise abstract (max {num_points} sentences) for the following article:\n\n{text}"
    elif style == "simple":
        prompt = f"Summarize this for a 12-year-old in {num_points} simple sentences:\n\n{text}"
    else:
        raise ValueError("Unknown style")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a clear, factual summarizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=350
    )
    return response.choices[0].message["content"].strip()

def ollama_summarize(model_name, text, style, num_points=5):
    if style == "bullet":
        prompt = f"Summarize the following text in {num_points} concise bullet points:\n\n{text}"
    elif style == "abstract":
        prompt = f"Write a concise abstract (max {num_points} sentences) for the following article:\n\n{text}"
    elif style == "simple":
        prompt = f"Summarize this for a 12-year-old in {num_points} simple sentences:\n\n{text}"
    else:
        raise ValueError("Unknown style")
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model_name, "prompt": prompt},
        stream=True
    )
    summary = ""
    for line in response.iter_lines():
        if line:
            try:
                obj = json.loads(line)
                if "response" in obj:
                    summary += obj["response"]
            except Exception:
                continue
    return summary.strip()

import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def extract_keywords(text):
    # Tokenize, lowercase, remove stopwords and short words
    tokens = re.findall(r'\b\w+\b', text.lower())
    keywords = set([token for token in tokens if token not in ENGLISH_STOP_WORDS and len(token) > 2])
    return keywords

def jaccard_score(source_text, summary_text):
    source_keywords = extract_keywords(source_text)
    summary_keywords = extract_keywords(summary_text)
    if not source_keywords or not summary_keywords:
        return 0.0
    overlap = source_keywords & summary_keywords
    union = source_keywords | summary_keywords
    return round(len(overlap) / len(union), 4)

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load model once at module level
embedder = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast, very good for English

def semantic_similarity(source_text, summary_text):
    source_emb = embedder.encode([source_text], convert_to_tensor=True)
    summary_emb = embedder.encode([summary_text], convert_to_tensor=True)
    score = cosine_similarity(source_emb, summary_emb)[0][0]
    return round(float(score), 4)

import pandas as pd
import datetime

def export_to_csv(summary_data, csv_path="summaries_log.csv"):
    # summary_data is a dict or list of dicts with the following keys:
    # ['file', 'model', 'style', 'num_points', 'summary', 'kw_score', 'sem_score', 'timestamp']
    df = pd.DataFrame([summary_data]) if isinstance(summary_data, dict) else pd.DataFrame(summary_data)
    # If CSV exists, append; else create new
    try:
        old = pd.read_csv(csv_path)
        df = pd.concat([old, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv(csv_path, index=False)
