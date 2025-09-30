# 📰 News Brief Generator

A multi-model, multi-style AI news/document summarizer with intuitive web interface, export, and evaluation metrics. Built for resumes, portfolio, and easy real-world use!

---

## 🔗 Live Demo

> [STREAMLIT APP LINK HERE](https://share.streamlit.io/your-username/news-brief-generator/main/streamlit_app.py) *(replace with your link)*

---

## ✨ Features

- **Summarize** text, PDF, and DOCX files
- **Model choice:** Groq, OpenAI, or Local (Ollama)
- **Summary styles:** bullet points, abstract, simple English (for kids)
- **Evaluation:** Keyword overlap (Jaccard) & Semantic similarity (embeddings)
- **Beautiful Perplexity-style dark UI**
- **Easy CSV export** for all results and scoring
- **Demo mode** for quick testing

---

## 🚀 Quick Start

1. **Install requirements**

    ```
    pip install -r requirements.txt
    ```

2. **(Optional) Local models**

    - [Install Ollama](https://ollama.com/) and run e.g. `ollama run llama3`

3. **Set API keys (`.env` or your server/Streamlit Cloud settings):**
    - `openai_api_key=...`
    - `groq_api_key=...`

4. **Run app locally**
    ```
    streamlit run streamlit_app.py
    ```

5. **Deploy to [Streamlit Cloud](https://streamlit.io/cloud) (Free for small apps)**
    - Push to GitHub, launch via Streamlit Cloud, set keys in secrets.

---

## ⚙️ Requirements

Included in `requirements.txt`:

streamlit
pandas
pdfplumber
python-docx
sentence-transformers
scikit-learn
openai
requests
groq


> If using local models, you need [Ollama](https://ollama.com/) installed.

---

## 🛡️ Security

- API keys should be stored securely as environment variables.
- Never commit `.env` or real keys to GitHub!

---

## 👨‍💻 Author

**Your Name**  
[Portfolio](https://your-portfolio-link) • [GitHub](https://your-github-link) • [LinkedIn](https://your-linkedin-link)

---

## 📜 License

MIT

