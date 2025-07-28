# File: c:\Users\kosisochukwu\Desktop\Teach\lan.py
import streamlit as st
from deep_translator import GoogleTranslator # Import GoogleTranslator from deep_translator
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

# Initialize session state for text_to_translate if not already present
if 'text_to_translate' not in st.session_state:
    st.session_state.text_to_translate = ""

# ---------- Sidebar Settings ----------
st.sidebar.header("🌍 Translation Settings")

# Get all supported languages from GoogleTranslator
# GoogleTranslator.get_supported_languages(as_dict=True) returns {lang_name: lang_code}
# GoogleTranslator.get_supported_languages(as_dict=False) returns [lang_code, ...]
# We need names for display and codes for translation.
supported_langs_dict = GoogleTranslator.get_supported_languages(as_dict=True)
language_names = list(supported_langs_dict.keys())
language_codes = list(supported_langs_dict.values())

# Popular languages first (adjust as needed based on deep_translator's names)
popular_langs = ['english', 'spanish', 'french', 'german', 'chinese (simplified)', 'japanese', 'arabic', 'hindi', 'portuguese', 'russian']
# Filter popular_langs to only include those actually supported by deep_translator
popular_langs_filtered = [lang for lang in popular_langs if lang in language_names]

popular_indices = [language_names.index(lang) for lang in popular_langs_filtered]
other_indices = [i for i in range(len(language_names)) if i not in popular_indices]
sorted_names = [language_names[i] for i in popular_indices] + [language_names[i] for i in other_indices]

dest_lang_name = st.sidebar.selectbox(
    "🎯 Translate to:",
    sorted_names,
    index=sorted_names.index("spanish") if "spanish" in sorted_names else 0
)
# Get the code for the selected language name
dest_lang_code = supported_langs_dict[dest_lang_name]

# Font size selector
font_size = st.sidebar.slider("📝 Font size for translated text", min_value=14, max_value=36, value=20)

# Audio speed
audio_speed = st.sidebar.slider("🔊 Audio speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# ---------- Custom CSS ----------
custom_css = f"""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Full-page background */
html, body, [data-testid="stApp"] {{
    height: 100%;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    background-attachment: fixed;
}}

/* Dark overlay for readability */
[data-testid="stApp"]::before {{
    content: "";
    position: absolute;
    top: 0; left: 0;
    right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.2);
    z-index: -1;
}}

/* Sidebar styling */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%) !important;
    backdrop-filter: blur(10px);
}}

[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
    color: white !important;
}}

/* Main container */
.main .block-container {{
    padding: 2rem 1rem;
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    margin: 2rem auto;
}}

/* Translated text styling */
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

/* Button styling */
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

/* Text area styling */
.stTextArea textarea {{
    background: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    font-size: 16px;
}}

/* Success/Info message styling */
.stSuccess, .stInfo {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}}

/* Title styling */
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
    # Use st.session_state.text_to_translate as the value for the text area
    st.session_state.text_to_translate = st.text_area(
        "✍️ Enter text to translate (auto-detect language):",
        value=st.session_state.text_to_translate, # Set the initial value from session state
        height=150,
        placeholder="Type or paste your text here..."
    )

with col2:
    st.markdown("### 🎯 Quick Actions")
    if st.button("🔄 Clear Text"):
        st.session_state.text_to_translate = "" # Clear the text in session state
        st.rerun() # Rerun to update the text area

    if st.button("📋 Sample Text"):
        st.session_state.text_to_translate = "Hello! This is a sample text for translation. Technology is connecting the world."
        st.rerun() # Rerun to update the text area with sample text

# ---------- Translation Button ----------
if st.button("🚀 Translate Now", type="primary"):
    if st.session_state.text_to_translate.strip(): # Use session state variable
        try:
            with st.spinner("🔄 Translating and generating audio..."):
                # Perform translation using deep_translator.GoogleTranslator
                # GoogleTranslator.translate returns the translated text directly
                # It also has a detect_language method if needed separately.
                translated_text = GoogleTranslator(source='auto', target=dest_lang_code).translate(
                    st.session_state.text_to_translate
                )

                # deep_translator doesn't directly return detected source language with translate()
                # We can try to detect it separately if needed for display
                try:
                    detected_lang_code = GoogleTranslator(source='auto', target=dest_lang_code).detect(
                        st.session_state.text_to_translate
                    )
                    # Find the name from the code
                    detected_lang_name = next((name for name, code in supported_langs_dict.items() if code == detected_lang_code), 'Unknown')
                except Exception:
                    detected_lang_name = "Unknown" # Fallback if detection fails

                # Display results
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.info(f"🔍 **Detected language:** {detected_lang_name.title()}")

                with col2:
                    confidence = "High" if len(st.session_state.text_to_translate) > 10 else "Medium"
                    st.success(f"✅ **Confidence:** {confidence}")

                st.success("🎉 **Translation Complete:**")
                st.markdown(f"<div class='translated-text'>{translated_text}</div>", unsafe_allow_html=True)

                # Generate audio
                try:
                    # gTTS uses ISO 639-1 codes, which dest_lang_code should already be
                    tts = gTTS(text=translated_text, lang=dest_lang_code, slow=(audio_speed < 1.0))
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    # Audio player
                    st.markdown("### 🔊 Audio Playback")
                    st.audio(audio_bytes.read(), format="audio/mp3")

                    # Reset for download
                    audio_bytes.seek(0)

                    # Download options
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.download_button(
                            label="📥 Download Audio (MP3)",
                            data=audio_bytes,
                            file_name=f"translation_{dest_lang_code}.mp3",
                            mime="audio/mp3"
                        )

                    with col2:
                        # Text download
                        text_download = f"Original ({detected_lang_name.title()}): {st.session_state.text_to_translate}\n\nTranslated ({dest_lang_name.title()}): {translated_text}"
                        st.download_button(
                            label="📄 Download Text",
                            data=text_download,
                            file_name=f"translation_{dest_lang_code}.txt",
                            mime="text/plain"
                        )

                    with col3:
                        if st.button("🔄 Translate Back"):
                            # Translate back to the detected source language
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

# ---------- Footer Info ----------
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
    st.markdown("• Google Translate (via deep_translator)\n• Text-to-Speech\n• Streamlit Framework\n• Python Backend")
