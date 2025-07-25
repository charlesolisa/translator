import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Tech Translator - Worldwide", 
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Supported Languages ----------
LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)
language_names = list(LANGUAGES.values())
language_codes = list(LANGUAGES.keys())

# ---------- Session State ----------
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# ---------- Sidebar Settings ----------
st.sidebar.header("🌍 Translation Settings")

# Popular language sorting
popular_langs = ['english', 'spanish', 'french', 'german', 'chinese (simplified)', 'japanese', 'arabic', 'hindi', 'portuguese', 'russian']
popular_indices = [language_names.index(lang) for lang in popular_langs if lang in language_names]
other_indices = [i for i in range(len(language_names)) if i not in popular_indices]
sorted_names = [language_names[i] for i in popular_indices] + [language_names[i] for i in other_indices]

dest_lang_name = st.sidebar.selectbox("🎯 Translate to:", sorted_names, index=sorted_names.index("spanish"))
dest_lang_code = list(LANGUAGES.keys())[language_names.index(dest_lang_name)]

font_size = st.sidebar.slider("📝 Font size for translated text", min_value=14, max_value=36, value=20)
audio_speed = st.sidebar.slider("🔊 Audio speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# ---------- Custom CSS ----------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [data-testid="stApp"] {{
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}}
[data-testid="stApp"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.2);
    z-index: -1;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9)) !important;
    backdrop-filter: blur(10px);
}}
.main .block-container {{
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    margin: 2rem auto;
}}
.translated-text {{
    font-size: {font_size}px;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8));
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    backdrop-filter: blur(10px);
}}
.stButton > button {{
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
    padding: 0.5rem 2rem;
    font-weight: 600;
}}
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    font-size: 16px;
}}
h1 {{
    color: white !important;
    text-align: center;
    font-weight: 700;
    margin-bottom: 2rem;
}}
</style>
""", unsafe_allow_html=True)

# ---------- App Title ----------
st.title("🌍 Tech Translator - Worldwide")
st.markdown("**Translate instantly to 100+ languages with audio support**")

# ---------- Input Area ----------
col1, col2 = st.columns([3, 1])
with col1:
    st.session_state.text_input = st.text_area(
        "✍️ Enter text to translate (auto-detect language):", 
        value=st.session_state.text_input,
        height=150,
        key="text_input_area",
        placeholder="Type or paste your text here..."
    )

with col2:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Clear Text"):
        st.session_state.text_input = ""
        st.experimental_rerun()
    if st.button("📋 Sample Text"):
        st.session_state.text_input = "Hello! This is a sample text for translation. Technology is connecting the world."
        st.experimental_rerun()

# ---------- Translate Button ----------
text_to_translate = st.session_state.text_input

if st.button("🚀 Translate Now", type="primary"):
    if text_to_translate.strip():
        try:
            with st.spinner("🔄 Translating and generating audio..."):
                translated_text = GoogleTranslator(source='auto', target=dest_lang_code).translate(text_to_translate)

                st.success("🎉 **Translation Complete:**")
                st.markdown(f"<div class='translated-text'>{translated_text}</div>", unsafe_allow_html=True)

                # Audio
                try:
                    tts = gTTS(text=translated_text, lang=dest_lang_code, slow=(audio_speed < 1.0))
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    st.markdown("### 🔊 Audio Playback")
                    st.audio(audio_bytes.read(), format="audio/mp3")
                    audio_bytes.seek(0)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button("📥 Download Audio (MP3)", audio_bytes, f"translation_{dest_lang_code}.mp3", "audio/mp3")
                    with col2:
                        text_download = f"Original:\n{text_to_translate}\n\nTranslated:\n{translated_text}"
                        st.download_button("📄 Download Text", text_download, f"translation_{dest_lang_code}.txt", "text/plain")
                    with col3:
                        if st.button("🔄 Translate Back"):
                            reverse = GoogleTranslator(source='auto', target='en').translate(translated_text)
                            st.info(f"**Reverse Translation:** {reverse}")

                except Exception as audio_error:
                    st.warning("⚠️ Audio generation failed.")
                    st.error(f"Audio error: {str(audio_error)}")
        except Exception as e:
            st.error("❌ Translation failed.")
            with st.expander("🔧 Error Details"):
                st.code(str(e))
    else:
        st.warning("⚠️ Please enter some text.")

# ---------- Footer ----------
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🌟 Features\n• 100+ Languages\n• Audio Playback\n• Auto-Detect\n• Download Options")
with col2:
    st.markdown("### ⚡ Performance\n• Fast Translation\n• High Accuracy\n• Responsive UI")
with col3:
    st.markdown("### 🔧 Tech Stack\n• Deep Translator\n• gTTS\n• Streamlit\n• Python")

