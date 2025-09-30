from summarizers import groq_summarize, openai_summarize, ollama_summarize, jaccard_score, semantic_similarity, export_to_csv
from dotenv import load_dotenv
import os
import pdfplumber
from docx import Document
import datetime

load_dotenv()
OPENAI_API_KEY = os.getenv("openai_api_key")
GROQ_API_KEY = os.getenv("groq_api_key")

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        with pdfplumber.open(file_path) as pdf:
            return "".join([page.extract_text() or "" for page in pdf.pages])
    elif ext == ".docx":
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type (.txt, .pdf, .docx)")

def truncate_text(text, max_words=4000):
    words = text.split()
    return " ".join(words[:max_words]) if len(words) > max_words else text

def main():
    api_choice = input("Enter the model to use (groq/openai/local): ").strip().lower()
    style = input("Choose summary style (bullet/abstract/simple): ").strip().lower()
    num_points = int(input("How many points/sentences? (default 5): ") or 5)
    file_path = input("Enter path to your file (.txt, .pdf, .docx): ").strip()
    text = extract_text_from_file(file_path).strip()
    text = truncate_text(text, max_words=4000)
    if not text:
        print("Couldn't extract any text from the file!")
        return

    if api_choice == "groq":
        try:
            from groq import Groq
            client = Groq(api_key=GROQ_API_KEY)
        except ImportError:
            print("Please install the 'groq' Python package.")
            return
        summary = groq_summarize(client, text, style, num_points)
    elif api_choice == "openai":
        summary = openai_summarize(text, style, num_points, OPENAI_API_KEY)
    elif api_choice == "local":
        model_name = input("Enter local model name (e.g. llama3, mistral, phi3): ").strip()
        summary = ollama_summarize(model_name, text, style, num_points)
    else:
        raise ValueError("Unknown API/model choice")

    print("\n--- SUMMARY ---\n")
    print(summary)

    kw_score = jaccard_score(text, summary)
    print(f"\n[Keyword Overlap Score: {kw_score}]")

    sem_score = semantic_similarity(text, summary)
    print(f"[Semantic Similarity Score: {sem_score}]")

    summary_data = {
        "file": file_path,
        "model": api_choice,
        "style": style,
        "num_points": num_points,
        "summary": summary,
        "kw_score": kw_score,
        "sem_score": sem_score,
        "timestamp": datetime.datetime.now().isoformat()
    }
    export_to_csv(summary_data)
    print(f"\nResults exported to summaries_log.csv")

if __name__ == "__main__":
    main()
