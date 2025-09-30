# 📰 Project 5/20 – News Brief Generator (AI-Powered Summarizer)

*Part of my **100 Days of Code – Portfolio Project Series***

# 📰 News Brief Generator

A multi-model, multi-style AI news/document summarizer with intuitive web interface, export, and evaluation metrics. Built for resumes, portfolio, and easy real-world use!

---

## 🔗 Live Demo

> [STREAMLIT APP LINK HERE](https://newsbriefgenerator-emdafmyzq3jq47bhqzpotw.streamlit.app/)

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

## 🛠 Tech Stack

- **Frontend/UI**: Streamlit  
- **Backend/AI**: Groq, OpenAI, Ollama (local LLMs)  
- **Evaluation**: Keyword matching, semantic similarity (embeddings)  
- **Deployment**: Streamlit Cloud 

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

📚 Learning Outcomes

Through this project, I learned:

How to build an end-to-end AI app (backend + frontend integration)

Streamlit best practices for building custom UIs

Deploying and scaling apps on the cloud (Streamlit Cloud)

Fundamentals of model benchmarking & explainable AI

---

## 🛡️ Security

- API keys should be stored securely as environment variables.
- Never commit `.env` or real keys to GitHub!

---

🤝 Contributing

Contributions are welcome!

Report bugs or suggest improvements via Issues

Fork and submit PRs with new features or fixes

---

## 👨‍💻 Author

**Kaustubh Mukdam**  
[Portfolio](https://portfolio-website-drab-kappa-33.vercel.app/) • [GitHub](https://github.com/KaustubhMukdam) • [LinkedIn](https://www.linkedin.com/in/kaustubh-mukdam-ab0170340/)

---

## 📜 License

MIT

