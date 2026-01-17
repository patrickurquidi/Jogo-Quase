import streamlit as st
import time
import random

st.set_page_config(page_title="QUASE", layout="centered")

st.title("🎯 QUASE")
st.write("Chegue o mais perto possível do centro.")

# Estado inicial
if "position" not in st.session_state:
    st.session_state.position = 0.0
    st.session_state.running = False
    st.session_state.best = 0.0
    st.session_state.start_time = time.time()
    st.session_state.speed = random.uniform(0.3, 0.8)

# Barra visual
target = 0.5  # centro
progress = st.session_state.position

st.progress(progress)

# Lógica de movimento
if st.session_state.running:
    elapsed = time.time() - st.session_state.start_time
    st.session_state.position = abs((elapsed * st.session_state.speed) % 1)

# Botões
col1, col2 = st.columns(2)

with col1:
    if st.button("▶️ Começar"):
        st.session_state.running = True
        st.session_state.start_time = time.time()
        st.session_state.speed = random.uniform(0.3, 0.8)

with col2:
    if st.button("⏹️ Parar"):
        st.session_state.running = False
        distance = abs(st.session_state.position - target)
        score = max(0, 100 - distance * 200)
        st.session_state.best = max(st.session_state.best, score)

        st.subheader(f"Quase: {score:.2f}%")
        st.write(f"Melhor da sessão: {st.session_state.best:.2f}%")

        # Reset posição
        st.session_state.position = 0.0
