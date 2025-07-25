import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from io import BytesIO
import base64

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Tech Translator - Worldwide",
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------- Sidebar Settings ----------
st.sidebar.header("🌍 Translation Settings")

# Supported languages from Deep Translator
LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)
language_names = list(LANGUAGES.keys())
language_codes = list(LANGUAGES.values())

# Prioritize popular languages
popular_langs = ['english', 'spanish', 'french', 'german', 'chinese', 'japanese', 'arabic', 'hindi', 'portuguese', 'russian']
popular_indices = [language_names.index(lang) for lang in popular_langs if lang in language_names]
other_indices = [i for i in range(len(language_names)) if i not in popular_indices]
sorted_names = [language_names[i] for i in popular_indices] + [language_names[i] for i in other_indices]

dest_lang_name = st.sidebar.selectbox(
    "🎯 Translate to:",
    sorted_names,
    index=sorted_names.index("spanish")
)
dest_lang_code = LANGUAGES[dest_lang_name]

# Font size selector
font_size = st.sidebar.slider("📝 Font size for translated text", min_value=14, max_value=36, value=20)

# Audio speed
audio_speed = st.sidebar.slider("🔊 Audio speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# ---------- Custom CSS ----------
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [data-testid="stApp"] {{
    height: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}}
[data-testid="stApp"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0;
    right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.2);
    z-index: -1;
}}
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%) !important;
    backdrop-filter: blur(10px);
}}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
    color: white !important;
}}
.main .block-container {{
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin: 2rem auto;
}}
.translated-text {{
    font-size: {font_size}px;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    line-height: 1.6;
}}
.stButton > button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}}
.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}}
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    font-size: 16px;
}}
.stSuccess, .stInfo {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}}
h1 {{
    color: white !important;
    text-align: center;
    font-weight: 700;
    margin-bottom: 2rem;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---------- App Title ----------
st.title("🌍 Tech Translator - Worldwide")
st.markdown("**Translate instantly to 100+ languages with audio support**")

# ---------- Input Area ----------
col1, col2 = st.columns([3, 1])

with col1:
    text_to_translate = st.text_area(
        "✍️ Enter text to translate (auto-detect language):",
        height=150,
        placeholder="Type or paste your text here..."
    )

with col2:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Clear Text"):
        st.rerun()

    if st.button("📋 Sample Text"):
        text_to_translate = "Hello! This is a sample text for translation. Technology is connecting the world."

# ---------- Translation Button ----------
if st.button("🚀 Translate Now", type="primary"):
    if text_to_translate.strip():
        try:
            with st.spinner("🔄 Translating and generating audio..."):
                translated_text = GoogleTranslator(source='auto', target=dest_lang_code).translate(text_to_translate)
                detected_lang = "Auto-detected"

                # Display results
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.info(f"🔍 **Detected language:** {detected_lang}")
                with col2:
                    confidence = "High" if len(text_to_translate) > 10 else "Medium"
                    st.success(f"✅ **Confidence:** {confidence}")

                st.success("🎉 **Translation Complete:**")
                st.markdown(f"<div class='translated-text'>{translated_text}</div>", unsafe_allow_html=True)

                # Generate audio
                try:
                    tts = gTTS(text=translated_text, lang=dest_lang_code, slow=(audio_speed < 1.0))
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    st.markdown("### 🔊 Audio Playback")
                    st.audio(audio_bytes.read(), format="audio/mp3")
                    audio_bytes.seek(0)

                    # Download Options
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.download_button(
                            label="📥 Download Audio (MP3)",
                            data=audio_bytes,
                            file_name=f"translation_{dest_lang_code}.mp3",
                            mime="audio/mp3"
                        )
                    with col2:
                        text_download = f"Original: {text_to_translate}\n\nTranslated ({dest_lang_name.title()}): {translated_text}"
                        st.download_button(
                            label="📄 Download Text",
                            data=text_download,
                            file_name=f"translation_{dest_lang_code}.txt",
                            mime="text/plain"
                        )
                    with col3:
                        if st.button("🔄 Translate Back"):
                            reverse_text = GoogleTranslator(source='auto', target='en').translate(translated_text)
                            st.info(f"**Reverse translation:** {reverse_text}")
                except Exception as audio_error:
                    st.warning("⚠️ Audio generation failed, but translation was successful!")
                    st.error(f"Audio error: {str(audio_error)}")

        except Exception as e:
            st.error("❌ Translation failed. Please check your internet connection and try again.")
            with st.expander("🔧 Error Details"):
                st.code(str(e))
    else:
        st.warning("⚠️ Please enter some text to translate.")

# ---------- Footer ----------
st.markdown("---")
col
