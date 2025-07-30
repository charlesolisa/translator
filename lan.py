# File: lan.py
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

# ---------- Session Initialization ----------
if 'text_to_translate' not in st.session_state:
    st.session_state.text_to_translate = ""

# ---------- Sidebar ----------
st.sidebar.header("🌍 Translation Settings")

translator_instance = GoogleTranslator()
supported_langs_dict = translator_instance.get_supported_languages(as_dict=True)
language_names = list(supported_langs_dict.keys())
language_codes = list(supported_langs_dict.values())

popular_langs = ['english', 'spanish', 'french', 'german', 'chinese (simplified)', 'japanese', 'arabic', 'hindi', 'portuguese', 'russian']
popular_langs_filtered = [lang for lang in popular_langs if lang in language_names]
popular_indices = [language_names.index(lang) for lang in popular_langs_filtered]
other_indices = [i for i in range(len(language_names)) if i not in popular_indices]
sorted_names = [language_names[i] for i in popular_indices] + [language_names[i] for i in other_indices]

dest_lang_name = st.sidebar.selectbox("🎯 Translate to:", sorted_names, index=sorted_names.index("spanish"))
dest_lang_code = supported_langs_dict[dest_lang_name]

font_size = st.sidebar.slider("📝 Font size for translated text", min_value=14, max_value=36, value=20)
audio_speed = st.sidebar.slider("🔊 Audio speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# ---------- Custom Dark Theme CSS ----------
custom_css = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [data-testid="stApp"] {{
    height: 100%;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #eee !important;
}}

[data-testid="stSidebar"] {{
    background: rgba(102, 126, 234, 0.9) !important;
    color: #eee !important;
}}

[data-testid="stSidebar"] * {{
    color: #eee !important;
}}

.stTextArea textarea {{
    background: rgba(255,255,255,0.1) !important;
    color: #fff !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    font-size: 16px;
    border-radius: 10px;
}}

.stButton > button {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: #fff !important;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 2rem;
    box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}}

.translated-text {{
    font-size: {font_size}px;
    font-weight: 600;
    color: #fff;
    background: rgba(118, 75, 162, 0.8);
    padding: 20px;
    border-radius: 15px;
    margin: 15px 0;
    border: 1px solid rgba(255, 255, 255, 0.2);
    line-height: 1.6;
}}

h1 {{
    color: #fff !important;
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
    st.session_state.text_to_translate = st.text_area(
        "✍️ Enter text to translate (auto-detect language):",
        value=st.session_state.text_to_translate,
        height=150,
        placeholder="Type or paste your text here..."
    )

with col2:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Clear Text"):
        st.session_state.text_to_translate = ""
        st.rerun()
    if st.button("📋 Sample Text"):
        st.session_state.text_to_translate = "Hello! This is a sample text for translation. Technology is connecting the world."
        st.rerun()

# ---------- Translate ----------
if st.button("🚀 Translate Now", type="primary"):
    if st.session_state.text_to_translate.strip():
        try:
            with st.spinner("🔄 Translating and generating audio..."):
                translated_text = GoogleTranslator(source='auto', target=dest_lang_code).translate(
                    st.session_state.text_to_translate
                )

                try:
                    detected_lang_code = GoogleTranslator(source='auto', target=dest_lang_code).detect(
                        st.session_state.text_to_translate
                    )
                    detected_lang_name = next((name for name, code in supported_langs_dict.items() if code == detected_lang_code), 'Unknown')
                except Exception:
                    detected_lang_name = "Unknown"

                st.success("🎉 **Translation Complete:**")
                st.markdown(f"<div class='translated-text'>{translated_text}</div>", unsafe_allow_html=True)

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
                        st.download_button(
                            label="📥 Download Audio (MP3)",
                            data=audio_bytes,
                            file_name=f"translation_{dest_lang_code}.mp3",
                            mime="audio/mp3"
                        )
                    with col2:
                        text_download = f"Original ({detected_lang_name.title()}): {st.session_state.text_to_translate}\n\nTranslated ({dest_lang_name.title()}): {translated_text}"
                        st.download_button(
                            label="📄 Download Text",
                            data=text_download,
                            file_name=f"translation_{dest_lang_code}.txt",
                            mime="text/plain"
                        )
                    with col3:
                        if st.button("🔄 Translate Back"):
                            reverse_translated_text = GoogleTranslator(source='auto', target=detected_lang_code).translate(
                                translated_text
                            )
                            st.info(f"**Reverse translation:** {reverse_translated_text}")

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
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("### 🌟 Features")
    st.markdown("• 100+ Languages\n• Audio Playback\n• Auto-Detection\n• Download Options")
with col2:
    st.markdown("### ⚡ Performance")
    st.markdown("• Real-time Translation\n• High Accuracy\n• Fast Processing\n• Mobile Friendly")
with col3:
    st.markdown("### 🔧 Tech Stack")
    st.markdown("• Google Translate\n• Text-to-Speech\n• Streamlit\n• Python")
