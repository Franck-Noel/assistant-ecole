import streamlit as st
import requests
import time
from streamlit_mic_recorder import speech_to_text

st.set_page_config(page_title="Assistant ENSEA", page_icon="🎓", layout="wide")

# Style personnalisé
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stChatMessage { border-radius: 12px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://ensai.fr/wp-content/uploads/2019/07/logo_ENSEA.png", width=180)
    st.title("Assistant ENSEA")
    st.info("🌐 Version Cloud (Gemini 2.5 Flash)")
    st.caption("Cette version utilise l'intelligence artificielle de Google pour une réponse rapide.")

    st.divider()
    st.subheader("Contacts ENSEA")
    st.write("📞 01 41 96 37 01")
    st.write("📧 francknoel.fogaing@ensea.edu.ci")
    
    if st.button("Réinitialiser le chat"):
        st.session_state.messages = []
        st.rerun()

# --- CHAT ---
st.title("🎓 Assistant ENSEA d'Abidjan")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="🎓" if msg["role"]=="assistant" else "👤"):
        st.markdown(msg["content"])

# --- SAISIE HYBRIDE ---
col_text, col_mic = st.columns([0.9, 0.1])

with col_mic:
    # Micro pour le vocal
    vocal_input = speech_to_text(language='fr', start_prompt="🎤", stop_prompt="🛑", key='mic')

with col_text:
    clavier_input = st.chat_input("Posez votre question ici...")

# Logique de détection d'entrée
prompt = vocal_input if vocal_input else clavier_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🎓"):
        placeholder = st.empty()
        try:
            with st.spinner("Recherche dans les documents de l'ENSEA..."):
                payload = {"message": prompt, "history": [], "mode": "Cloud (Gemini)"}
                r = requests.post("http://127.0.0.1:8000/chat", json=payload)
                full_text = r.json()["response"]
            
            # Animation de réponse
            displayed = ""
            for word in full_text.split():
                displayed += word + " "
                placeholder.markdown(displayed + "▌")
                time.sleep(0.02)
            placeholder.markdown(displayed)
            st.session_state.messages.append({"role": "assistant", "content": displayed})
            
        except:
            st.error("Le serveur backend ne répond pas. Vérifiez qu'il est bien lancé.")