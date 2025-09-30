import streamlit as st
import datetime
import pandas as pd
import os
from summarizers import groq_summarize, openai_summarize, ollama_summarize, jaccard_score, semantic_similarity

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="News Brief Generator",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- DARK THEME STYLE ---
def set_dark_theme():
    st.markdown("""
    <style>
    body, .reportview-container {
        background-color: #12141b;
        color: #cdd2e8;
    }
    .sidebar .sidebar-content {background-color:#1a1b22;}
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #181a24 !important;
        color: #cdd2e8 !important;
        border: 1px solid #3c4352 !important;
    }
    .stButton>button, .stDownloadButton>button {
        background-color: #2047a0;
        color: white;
        border-radius:8px;
    }
    .stFileUploader>div>div>div>button {
        background-color: #0653b6;
        color: white;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #68dfff;
    }
    /* Custom summary box */
    .summary-box {
        background: #232744;
        border-radius:6px;
        padding:16px;
        color: #cdd2e8 !important;
        font-size:1.05rem;
        margin-bottom: 1em;
        line-height: 1.7;
        word-break: break-word;
    }
    </style>
    """, unsafe_allow_html=True)
    
set_dark_theme()

# --- SIDEBAR: ABOUT, LINKS, THEME ---
with st.sidebar:
    st.image("logo.jpg", width=120)  
    st.title("About")
    st.markdown("""
        **News Brief Generator** lets you create AI summaries for any article or document!
        - Summarizes .txt, .pdf, .docx files.
        - Choose from Groq, OpenAI, or Local (Ollama) models.
        - Three summary styles: bullet, abstract, simple-English.
        - Shows both keyword overlap and semantic similarity scores.
        - Download CSV report of your runs.
    """, unsafe_allow_html=True)
    st.markdown('---')
    st.markdown("🌐 [Portfolio](https://your-portfolio-link) &nbsp;|&nbsp; [GitHub](https://your-github-link) &nbsp;|&nbsp; [LinkedIn](https://your-linkedin-link)")
    theme_mode = st.radio("Theme", ["Dark"], index=0)  # (More can be added, Streamlit theming is limited currently)

# --- MAIN TITLE ---
st.markdown("<h1 style='color:#68dfff; text-align:center;'>📰 News Brief Generator</h1>", unsafe_allow_html=True)
st.write("Summarize articles with AI. Choose your model, style, and see evaluation scores. Download results as CSV for cross-comparison or reporting.")

# --- DEMO SECTION ---
demo_button = st.button("Try Demo Article")
if demo_button:
    demo_text = (
        "Apple has announced the release of the iPhone 16 at its September event. "
        "Features include a 200MP camera, AI battery manager, satellite connectivity. Tim Cook says it's the 'smartest, greenest iPhone yet.' "
        "Pre-orders start Oct 1, available in stores Oct 15."
    )
    st.code(demo_text, language="markdown")

# --- FILE UPLOAD AND PARAMS ---
uploaded_file = st.file_uploader("Upload .txt, .pdf, or .docx file", type=["txt", "pdf", "docx"])
model_choice = st.selectbox("Choose model", ["groq", "openai", "local"], index=0)
summary_style = st.selectbox("Summary style", ["bullet", "abstract", "simple"], index=0)
num_points = st.number_input("Number of points/sentences", min_value=1, max_value=20, value=5)

model_name = None
if model_choice == "local":
    model_name = st.text_input("Local model name (e.g. llama3, mistral, phi3):", value="llama3")

# --- EXTRACT TEXT FUNCTION ---
def extract_text_from_file(file):
    import pdfplumber
    from docx import Document
    ext = os.path.splitext(file.name)[1].lower()
    if ext == ".txt":
        return file.read().decode("utf-8")
    elif ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            return "".join([page.extract_text() or "" for page in pdf.pages])
    elif ext == ".docx":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError("Unsupported file type.")

def truncate_text(text, max_words=4000):
    words = text.split()
    return " ".join(words[:max_words]) if len(words) > max_words else text

# --- SESSION STORAGE FOR CSV EXPORT ---
if "runs" not in st.session_state:
    st.session_state["runs"] = []

# --- MAIN RUN: GENERATE SUMMARY ---
if st.button("Generate Summary") and (uploaded_file or demo_button):
    try:
        with st.spinner("Processing..."):
            if uploaded_file:
                text = extract_text_from_file(uploaded_file).strip()
                file_name = uploaded_file.name
            else:
                text = demo_text
                file_name = "demo_article.txt"
            text = truncate_text(text, max_words=4000)

            # --- Model Call ---
            summary = ""
            if model_choice == "groq":
                from groq import Groq
                groq_key = os.environ.get("groq_api_key")
                client = Groq(api_key=groq_key)
                summary = groq_summarize(client, text, summary_style, num_points)
            elif model_choice == "openai":
                openai_key = os.environ.get("openai_api_key")
                summary = openai_summarize(text, summary_style, num_points, openai_key)
            elif model_choice == "local":
                summary = ollama_summarize(model_name, text, summary_style, num_points)

            kw_score = jaccard_score(text, summary)
            sem_score = semantic_similarity(text, summary)

            # --- DISPLAY ---
            st.markdown("### Your Summary")
            st.markdown(f"<div class='summary-box'>{summary.replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<b>Keyword Overlap Score:</b> <span style='color:#68dfff'>{kw_score}</span> &nbsp; | &nbsp; "
                f"<b>Semantic Similarity:</b> <span style='color:#68dfff'>{sem_score}</span>",
                unsafe_allow_html=True
            )
            st.code(summary, language="markdown")  # for easy copy

            # --- CSV Export Logic ---
            summary_data = {
                "file": file_name,
                "model": model_choice,
                "style": summary_style,
                "num_points": num_points,
                "summary": summary,
                "kw_score": kw_score,
                "sem_score": sem_score,
                "timestamp": datetime.datetime.now().isoformat()
            }
            st.session_state["runs"].append(summary_data)
            df = pd.DataFrame(st.session_state["runs"])
            st.download_button(
                "Download CSV of all runs",
                df.to_csv(index=False),
                file_name="summaries_log.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<small style='color:#68dfff;'>Made with ❤️ for your portfolio | Powered by Groq, OpenAI, Ollama, and Streamlit</small>", unsafe_allow_html=True)
