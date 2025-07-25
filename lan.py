import streamlit as st
from googletrans import Translator, LANGUAGES
from gtts import gTTS
from io import BytesIO

# ---------- Page Setup ----------
st.set_page_config(
    page_title="Tech Translator - Worldwide", 
    page_icon="🌍",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Initialize translator
translator = Translator()

# ---------- Sidebar Mode Selector ----------
mode = st.sidebar.radio(
    "Select Mode:",
    ("Translate Text", "Learn Languages")
)

# ---------- Custom CSS as before ----------
# (Include your custom CSS here, unchanged)
# For brevity, omitted here, but include your previous custom_css markdown.

# ---------- Main Content ----------
if mode == "Translate Text":
    # Existing translation UI code
    st.title("🌍 Tech Translator - Worldwide")
    st.markdown("**Translate instantly to 100+ languages with audio support**")
    
    # Language selection
    language_names = list(LANGUAGES.values())
    language_codes = list(LANGUAGES.keys())
    popular_langs = ['english', 'spanish', 'french', 'german', 'chinese', 'japanese', 'arabic', 'hindi', 'portuguese', 'russian']
    popular_indices = [language_names.index(lang) for lang in popular_langs if lang in language_names]
    other_indices = [i for i in range(len(language_names)) if i not in popular_indices]
    sorted_names = [language_names[i] for i in popular_indices] + [language_names[i] for i in other_indices]

    dest_lang_name = st.sidebar.selectbox(
        "🎯 Translate to:", 
        sorted_names, 
        index=sorted_names.index("spanish")
    )
    dest_lang_code = language_codes[language_names.index(dest_lang_name)]

    font_size = st.sidebar.slider("📝 Font size for translated text", min_value=14, max_value=36, value=20)
    audio_speed = st.sidebar.slider("🔊 Audio speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

    # Input area
    col1, col2 = st.columns([3, 1])
    with col1:
        text_to_translate = st.text_area("✍️ Enter text to translate (auto-detect language):", height=150, placeholder="Type or paste your text here...")
    with col2:
        st.markdown("### 🎯 Quick Actions")
        if st.button("🔄 Clear Text"):
            st.experimental_rerun()
        if st.button("📋 Sample Text"):
            text_to_translate = "Hello! This is a sample text for translation. Technology is connecting the world."

    # Translate button
    if st.button("🚀 Translate Now", type="primary"):
        if text_to_translate.strip():
            try:
                with st.spinner("🔄 Translating and generating audio..."):
                    translated = translator.translate(text_to_translate, dest=dest_lang_code)
                    translated_text = translated.text
                    detected_lang = LANGUAGES.get(translated.src, 'Unknown').title()

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
                        # Download options
                        st.download_button(
                            label="📥 Download Audio (MP3)",
                            data=audio_bytes,
                            file_name=f"translation_{dest_lang_code}.mp3",
                            mime="audio/mp3"
                        )
                        # Download text
                        text_download = f"Original ({detected_lang}): {text_to_translate}\n\nTranslated ({dest_lang_name.title()}): {translated_text}"
                        st.download_button(
                            label="📄 Download Text",
                            data=text_download,
                            file_name=f"translation_{dest_lang_code}.txt",
                            mime="text/plain"
                        )
                        # Reverse translation
                        if st.button("🔄 Translate Back"):
                            reverse_translated = translator.translate(translated_text, dest=translated.src)
                            st.info(f"**Reverse translation:** {reverse_translated.text}")
                    except Exception as audio_error:
                        st.warning("⚠️ Audio generation failed, but translation was successful!")
                        st.error(f"Audio error: {str(audio_error)}")
            except Exception as e:
                st.error("❌ Translation failed. Please check your internet connection and try again.")
                st.expander("🔧 Error Details").code(str(e))
        else:
            st.warning("⚠️ Please enter some text to translate.")

elif mode == "Learn Languages":
    # New section for learning
    st.title("📚 Learn Languages")
    st.markdown("**Basic vocabulary, common phrases, and pronunciation tips.**")
    
    # Example lessons or vocabulary
    # You could load from a data file or API for more dynamic content
    lessons = {
        "Spanish": {
            "Greetings": ["Hola - Hello", "Buenos días - Good morning", "Gracias - Thank you"],
            "Common Phrases": ["¿Cómo estás? - How are you?", "Por favor - Please", "Lo siento - Sorry"]
        },
        "French": {
            "Greetings": ["Bonjour - Hello", "Bon après-midi - Good afternoon", "Merci - Thank you"],
            "Common Phrases": ["Comment ça va? - How are you?", "S'il vous plaît - Please", "Désolé - Sorry"]
        },
        "Japanese": {
            "Greetings": ["こんにちは (Konnichiwa) - Hello", "おはようございます (Ohayō gozaimasu) - Good morning", "ありがとう (Arigatou) - Thank you"],
            "Common Phrases": ["お元気ですか？ (Ogenki desu ka?) - How are you?", "お願いします (Onegaishimasu) - Please", "すみません (Sumimasen) - Sorry"]
        }
        # Add more languages and lessons as needed
    }

    selected_language = st.selectbox("Choose a language to learn:", list(lessons.keys()))
    lessons_for_lang = lessons[selected_language]
    for topic, phrases in lessons_for_lang.items():
        st.subheader(topic)
        for phrase in phrases:
            st.markdown(f"- {phrase}")
        st.markdown("---")
    
    st.info("Practice these phrases to improve your language skills!")

# Optional: add more features like pronunciation audio, quizzes, or interactive lessons